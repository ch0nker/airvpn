from airvpn.web.services.common import ClientService, WebSession
from .models import Port, PortSession
from airvpn.web.services.devices import DeviceKey

from airvpn.exceptions import InvalidPort

from typing import Literal

import time

class PortManager(ClientService):
    """Manages the authenticated user's forwarded ports on AirVPN.

    Wraps the AJAX endpoints behind ``https://airvpn.org/ports/`` to list,
    open, close, and edit forwarded ports, as well as inspect active
    sessions on a port. Any mutating action (`open`, `close`, `edit`)
    triggers a poll loop afterward, since AirVPN applies these changes
    asynchronously on the server side.

    Attributes:
        session (WebSession): The authenticated web session used for all
            requests made by this manager.
        ecsrf (str | None): CSRF token scraped from the ports page, used to
            authorize AJAX requests. Lazily fetched on first use.
        pool (str | None): Identifier of the port pool the user belongs to,
            as reported by the manifest.
        ports (list[Port]): All ports currently owned by the user.
        keys (list[Key]): Keys associated with the user's ports, as reported
            by the manifest.
    """

    __URL__ = "https://airvpn.org/ports/"

    def __init__(self, session: WebSession):
        super().__init__(PortManager.__URL__, session)
        self.pool = None
        self.ports: list[Port] = []
        self.keys: list[DeviceKey] = []
        self._port_map = {}

        self.update()

    def update(self):
        """Refresh the manager's state from the server manifest.

        Fetches the current manifest and repopulates `pool`, `ports`,
        `keys`, and the internal port lookup map from the response.
        """
        self._get_ecsrf()
        manifest = self.request("manifest")
        self.pool = manifest.get("pool")

        self.ports = []
        self._port_map = {}
        for port in manifest.get("ports", []):
            port = Port(**port)
            self._port_map[port.port] = port
            self.ports.append(port)
    
        self.keys = [DeviceKey(**key) for key in manifest.get("keys", [])]

    def poll_update(self):
        while self.request("pending") == "1":
            time.sleep(3)

    def get(self, port: int):
        return self._port_map.get(port)

    def __getitem__(self, port: int) -> None | Port:
        return self.get(port)

    def edit(self, port: int | Port,
             device: str | None = None,
             note: str | None = None,
             protocol: Literal["both", "udp", "tcp"] | None = None,
             localport: int | None = None,
             ddns: str | None = None,
             layer: Literal["both", "v6", "v4"] | None = None):
        """Edit one or more attributes of an existing forwarded port.

        Only fields that are not ``None`` are sent as edit requests. After
        submitting the requested edits, blocks until the server finishes
        applying them.

        Args:
            port: Port number or `Port` instance to edit.
            device: New device name to associate with the port.
            note: New note/description for the port.
            protocol: New protocol restriction (``"both"``, ``"udp"``, or
                ``"tcp"``).
            localport: New local port to forward to.
            ddns: New dynamic DNS hostname for the port.
            layer: New IP layer restriction (``"both"``, ``"v6"``, or
                ``"v4"``).
        """
        port_number = port

        if isinstance(port, Port):
            port_number = port.port
        else:
            port = self[port_number]

        def edit_request(name, value):
            self.edit_request(name, value,
                pool=port.pool,
                port=port_number)

        if device is not None:
            edit_request("device", device)
            port.device = device

        if note is not None:
            edit_request("note", note)
            port.notes = note

        if protocol is not None:
            edit_request("protocol", protocol)
            port.protocol = protocol

        if localport is not None:
            edit_request("localport", localport)
            port.local = localport

        if ddns is not None:
            edit_request("ddns", ddns)
            port.dns = ddns

        if layer is not None:
            edit_request("layer", layer)
            port.iplayer = layer

        self.poll_update()

    def open(self, port: int | None = None) -> Port:
        """Open (forward) a new port.

        Args:
            port: Port number to open. Must be ``>= 2048`` and not already
                in use.

        Returns:
            Port: The newly created `Port` instance.

        Raises:
            InvalidPort: If `port` is below 2048, or is already in use.
        """
        if port is not None and port < 2048:
            raise InvalidPort("You can use only ports >=2048, lower ports are already reserved.")

        if self[port] is not None:
            raise InvalidPort(f"The port {port} is already in use.")

        port = port or ""
        data = self.request("insert", port=port)
        self.poll_update()

        result = Port(**data)
        self.ports.append(result)
        self._port_map[result.port] = result

        return result

    def close(self, port: int | Port):
        """Close (delete) an existing forwarded port.

        Args:
            port: Port number or `Port` instance to close.

        Raises:
            InvalidPort: If the given port does not exist.
        """
        pool = self.pool
    
        if isinstance(port, Port):
            pool = port.pool
            port = port.port

        if self.get(port) is None:
            raise InvalidPort(f"Port {port} does not exist.")

        self.request("delete", port=port, pool=pool)
        self.poll_update()

    def get_sessions(self, port: int | Port) -> list[PortSession]:
        """Retrieve active sessions for a given port.

        Args:
            port: Port number or `Port` instance to query.

        Returns:
            list[PortSession]: Active sessions currently using the port.
        """
        if isinstance(port, Port):
            port = port.port

        data = self.request("sessions", port=port, pool=self.pool)
        return [PortSession(**session) for session in data.get("items", [])]

    def test_open(self, port: int | Port) -> list[str]:
        """Test which of a port's active TCP sessions are reachable.

        Fetches the sessions for `port` and, for each non-UDP session,
        issues a connectivity test against the session's server IP and
        port.

        Args:
            port: Port number or `Port` instance to test.

        Returns:
            list[Session]: The sessions that passed the connectivity test.
        """
        sessions = self.get_sessions(port)
        result = []

        for session in sessions:
            if session.protocol == "udp":
                continue

            data = self.request("test",
                                ip=session.server_ip,
                                port=session.port,
                                pool=session.pool,
                                protocol=session.protocol)

            if data.get("type", "error") == "error":
                continue

            result.append(session)

        return result

    def sequential_search(self, amount: int) -> int:
        """Search for a run of consecutive free ports.

        Asks the server to find `amount` consecutive unused ports.

        Args:
            amount: Number of consecutive free ports to search for.

        Returns:
            The starting port number of the free run, or ``0`` if no such
            run of free ports was found.
        """
        data = self.request("seq_search", n=amount)

        return data.get("port")

    def get_used_ports(self) -> list[int]:
        """Retrieve the list of currently used ports in the primary pool.

        Fetches usage data via the ``"graph"`` action and returns the ports
        from the first pool in the response.

        Returns:
            list[int]: Port numbers currently in use in the primary pool, or
                an empty list if the response contains no pool data.
        """
        data = self.request("graph")
        return data.get("pools", [[]])[0]

    def check_propagation(self,
                      ddns_name: str,
                      services = ["airvpn", "dnsadvantage", "cloudflare", "google", "opendns"]):
        """Check which DNS services have propagated a dynamic DNS record.

        Queries each service in `services` for the current IPv4/IPv6
        resolution of `ddns_name`, and collects the names of services that
        have already propagated the record (i.e. return a non-empty address).

        Args:
            ddns_name: The dynamic DNS hostname to check propagation for.
            services: Names of DNS services to check. Defaults to
                ``["airvpn", "dnsadvantage", "cloudflare", "google", "opendns"]``.

        Returns:
            list[str]: Names of the services that have propagated the record.
        """
        results = []
        for service in services:
            data = self.request("ddns_service",
                                service=service,
                                name=ddns_name)

            if data.get("ipv4") == "" and data.get("ipv6") == "":
                continue

            results.append(service)

        return results

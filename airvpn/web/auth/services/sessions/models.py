from typing import TypedDict, Unpack
from datetime import datetime, timezone


class SessionDict(TypedDict, total=False):
    i: int
    session_id: str
    device_id: str
    device_name: str
    device_description: str | None
    server_html: str
    connected_since: int
    bytes_write: int
    bytes_read: int
    speed_write: int
    speed_read: int
    software_name: str
    software_img: str
    last_handshake: str
    exit_ipv4: str
    exit_ipv6: str
    vpn_ipv4: str
    vpn_ipv6: str
    entry_layer: str
    dns_filter: str
    disconnect: int

class Session:
    """An active VPN connection session for one of the user's devices.

    Constructed from the session entries returned when listing a device's
    live connections.

    Attributes:
        index (int | None): Index of the session in the response list.
        session_id (str | None): Unique identifier of the session.
        device_id (str | None): Identifier of the connected device.
        device_name (str | None): Name of the connected device.
        device_description (str | None): Description of the connected
            device, if set.
        server_html (str | None): HTML snippet describing the connected
            server (e.g. name/flag markup), as returned by the server.
        connected_since (datetime): UTC timestamp of when the session
            started, converted from the response's Unix timestamp.
        bytes_write (int | None): Total bytes sent during the session.
        bytes_read (int | None): Total bytes received during the session.
        speed_write (int | None): Current upload speed, in bytes per
            second.
        speed_read (int | None): Current download speed, in bytes per
            second.
        software_name (str | None): Name of the client software used to
            connect.
        software_img (str | None): URL or path of an icon representing the
            client software.
        last_handshake (datetime): UTC timestamp of the most recent
            handshake, converted from the response's Unix timestamp string.
        exit_ipv4 (str | None): IPv4 address the session exits the VPN
            through.
        exit_ipv6 (str | None): IPv6 address the session exits the VPN
            through.
        vpn_ipv4 (str | None): IPv4 address assigned to the device within
            the VPN.
        vpn_ipv6 (str | None): IPv6 address assigned to the device within
            the VPN.
        entry_layer (str | None): IP layer used to connect to the entry
            server.
        dns_filter (str | None): Name of the DNS filtering profile applied
            to the session.
        disconnect (int | None): Flag/timestamp indicating whether and
            when the session was (or will be) disconnected.
    """

    def __init__(self, **kwargs: Unpack[SessionDict]):
        self.index = kwargs.get("i")
        self.session_id = kwargs.get("session_id")
        self.device_id = kwargs.get("device_id")
        self.device_name = kwargs.get("device_name")
        self.device_description = kwargs.get("device_description")
        self.server_html = kwargs.get("server_html")
        self.connected_since = datetime.fromtimestamp(kwargs.get("connected_since"), timezone.utc)
        self.bytes_write = kwargs.get("bytes_write")
        self.bytes_read = kwargs.get("bytes_read")
        self.speed_write = kwargs.get("speed_write")
        self.speed_read = kwargs.get("speed_read")
        self.software_name = kwargs.get("software_name")
        self.software_img = kwargs.get("software_img")
        self.last_handshake = datetime.fromtimestamp(int(kwargs.get("last_handshake")), timezone.utc)
        self.exit_ipv4 = kwargs.get("exit_ipv4")
        self.exit_ipv6 = kwargs.get("exit_ipv6")
        self.vpn_ipv4 = kwargs.get("vpn_ipv4")
        self.vpn_ipv6 = kwargs.get("vpn_ipv6")
        self.entry_layer = kwargs.get("entry_layer")
        self.dns_filter = kwargs.get("dns_filter")
        self.disconnect = kwargs.get("disconnect")
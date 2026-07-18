from airvpn.network import AirSession
from airvpn.devices import Devices, Device
from airvpn.dns_lists import DnsLists
from airvpn.generator import Generator
from airvpn.status import Status, Server
from airvpn.userinfo import UserInfo
from airvpn.whatismyip import WhatIsMyIp

from airvpn.disconnect import disconnect
from airvpn.notification import send_notification

class AirVPN:
    """Main entry point for interacting with the AirVPN API.

    Provides access to all available services (devices, DNS lists, config
    generator, network status, user info, and IP lookup) as lazily-created,
    cached properties, plus convenience methods for one-off actions like
    sending notifications and disconnecting sessions.

    Attributes:
        api_key: The API key used for authenticated requests, if provided.
        session: The underlying AirSession used to make API requests.
        devices: The devices service, created and cached on first access.
        dns_lists: The DNS lists service, created and cached on first access.
        generator: The config generator service, created and cached on
            first access.
        status: The network status service, created and cached on first
            access.
        userinfo: The user info service, created and cached on first access.
        whatismyip: The IP lookup service, created and cached on first
            access.
    """
    __service_classes__ = {
        "devices": Devices,
        "dns_lists": DnsLists,
        "generator": Generator,
        "status": Status,
        "userinfo": UserInfo,
        "whatismyip": WhatIsMyIp
    }

    def __init__(self, API_KEY: str = None):
        self.api_key = API_KEY
        self.session = AirSession(API_KEY)

        self._devices = None
        self._dns_lists = None
        self._generator = None
        self._status = None
        self._userinfo = None
        self._whatismyip = None

    def get_service(self, service: str):
        """Instantiate a named service class, enforcing its API key requirement.

        Args:
            service: The service name (e.g. "devices", "status"), matched
                case-insensitively against the registered service classes.

        Returns:
            An instance of the requested service class.

        Raises:
            AssertionError: If the service name is invalid.
            Exception: If the service requires an API key and none was provided.
        """
        service_class = AirVPN.__service_classes__.get(service.lower())
        assert service_class, f"Invalid service name: {service}"

        service = service_class(self.session)
        if service_class.KEY_NEEDED and not self.api_key:
            raise Exception(f"API key is required to use \"{service}\"")

        assert service, "Failed to create service"

        return service
    
    @property
    def devices(self) -> Devices:
        """The devices service, created and cached on first access."""
        if not self._devices:
            self._devices = self.get_service("devices")
        return self._devices

    @property
    def dns_lists(self) -> DnsLists:
        """The DNS lists service, created and cached on first access."""
        if not self._dns_lists:
            self._dns_lists = self.get_service("dns_lists")
        return self._dns_lists
    
    @property
    def generator(self) -> Generator:
        """The config generator service, created and cached on first access."""
        if not self._generator:
            self._generator = self.get_service("generator")
        return self._generator

    @property
    def status(self) -> Status:
        """The network status service, created and cached on first access."""
        if not self._status:
            self._status = self.get_service("status")
        return self._status

    @property
    def userinfo(self) -> UserInfo:
        """The user info service, created and cached on first access."""
        if not self._userinfo:
            self._userinfo = self.get_service("userinfo")
        return self._userinfo
    
    @property
    def whatismyip(self) -> WhatIsMyIp:
        """The IP lookup service, created and cached on first access."""
        if not self._whatismyip:
            self._whatismyip = self.get_service("whatismyip")
        return self._whatismyip
    
    def send_notification(self, subject: str, body: str):
        """Send a message to yourself.

        Args:
            subject: The notification's subject line.
            body: The notification's message content.

        Returns:
            True if the notification was sent successfully, False otherwise.

        Access type:
            User-specific, API KEY required.
        """
        assert self.api_key, "API key is required"

        return send_notification(self.session, subject, body)

    def disconnect(self,
                    server: Server = None,
                    device: Device = None,
                    server_name: str = None,
                    device_id: str = None):
        """Requests a disconnection. If none of the filter parameters is specified, disconnect all sessions of the user.

        Args:
            server: A Server object to disconnect from; its public_name is
                used if server_name is not explicitly provided.
            device: A Device object to disconnect; its id is used if
                device_id is not explicitly provided.
            server_name: Name of the server to disconnect from. Ignored if
                server is provided.
            device_id: ID of the device to disconnect. Ignored if device
                is provided.

        Returns:
            The number of sessions that were disconnected.

        Access type:
            User-specific, API KEY required.
        """
        assert self.api_key, "API key is required"

        disconnect(self.session, 
                   server_name=server.name if server else server_name,
                   device_id=device.id if device else device_id)
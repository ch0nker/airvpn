"""Wrapper for AirVPN's [REST API](https://airvpn.org/apisettings/)"""

from __future__ import annotations

__title__ = "API"
__all__ = ["AirVPN"]

from airvpn.api.devices import Devices, Device
from airvpn.api.dns_lists import DnsLists
from airvpn.api.generator import Generator
from airvpn.api.status import Status, Server
from airvpn.api.userinfo import UserInfo
from airvpn.api.whatismyip import WhatIsMyIp
from airvpn.api.notification import Notification

from airvpn.exceptions import APIKeyRequired, InvalidService

class AirVPN:
    """Main entry point for interacting with the AirVPN API.

    Provides access to all available services (devices, DNS lists, config
    generator, network status, user info, and IP lookup) as lazily-created,
    cached properties, plus convenience methods for one-off actions like
    sending notifications and disconnecting sessions.

    Attributes:
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
        "whatismyip": WhatIsMyIp,
        "notification": Notification
    }

    def __init__(self, api_key: str = None):
        from airvpn.api.network import AirSession

        self.session = AirSession(api_key)

        self._devices = None
        self._dns_lists = None
        self._generator = None
        self._status = None
        self._userinfo = None
        self._whatismyip = None
        self._notification = None

    def get_service(self, service: str) -> Devices | DnsLists | Generator | Status | UserInfo | WhatIsMyIp | Notification:
        """Instantiate a named service class, enforcing its API key requirement.

        Args:
            service: The service name (e.g. "devices", "status"), matched
                case-insensitively against the registered service classes.

        Returns:
            An instance of the requested service class.

        Raises:
            RateLimited: If too many requests go through.
            APIError: If the service request results in an error.
            InvalidService: If the service name is invalid.
            APIKeyRequired: If the service requires an API key and none was provided.
        """

        service_class = AirVPN.__service_classes__.get(service.lower())
        if service_class is None:
            raise InvalidService(f"Service \"{service}\" doesn't exist")

        service = service_class(self.session)
        if service_class.__KEY_NEEDED__ and self.api_key is None:
            raise APIKeyRequired(f"API key is required to use \"{service}\"")

        if service is None:
            raise InvalidService("Failed to create service")

        return service

    @property
    def notification(self) -> Notification:
        """The notification service"""
        if self._notification is None:
            self._notification = self.get_service("notification")
        return self._notification
    
    @property
    def devices(self) -> Devices:
        """The devices service"""
        if self._devices is None:
            self._devices = self.get_service("devices")
        return self._devices

    @property
    def dns_lists(self) -> DnsLists:
        """The DNS lists service"""
        if self._dns_lists is None:
            self._dns_lists = self.get_service("dns_lists")
        return self._dns_lists
    
    @property
    def generator(self) -> Generator:
        """The config generator service"""
        if self._generator is None:
            self._generator = self.get_service("generator")
        return self._generator

    @property
    def status(self) -> Status:
        """The network status service"""
        if self._status is None:
            self._status = self.get_service("status")
        return self._status

    @property
    def userinfo(self) -> UserInfo:
        """The user info service"""
        if self._userinfo is None:
            self._userinfo = self.get_service("userinfo")
        return self._userinfo
    
    @property
    def whatismyip(self) -> WhatIsMyIp:
        """The IP lookup service"""
        if self._whatismyip is None:
            self._whatismyip = self.get_service("whatismyip")
        return self._whatismyip

    def disconnect(self,
                    server: Server | str = None,
                    device: Device = None,
                    device_id: str = None) -> int:
        """Requests a disconnection. If none of the filter parameters is specified, disconnect all sessions of the user.

        Access type:
            User-specific, API KEY required.

        Args:
            server: A Server object or a server's public name to disconnect from
            device: A Device object to disconnect; its id is used if
                device_id is not explicitly provided.
            device_id: ID of the device to disconnect. Ignored if device
                is provided.

        Returns:
            Sessions disconnected.

        Raises:
            APIKeyRequired: If you don't set your api_key.
            APIError: If the API fails.
            RateLimited: If too many requests go through.

        """
        from airvpn.api.disconnect import disconnect

        if self.api_key is None:
            raise APIKeyRequired("API key is required")

        return disconnect(self.session, 
                   server_name=str(server),
                   device_id=device.id if device else device_id)

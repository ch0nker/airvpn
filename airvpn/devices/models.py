from typing import Unpack, TypedDict

class DeviceDict(TypedDict):
    id: str
    name: str
    description: str
    version: str
    renew_first_unix: int
    renew_first_date: str
    renew_last_unix: int
    renew_last_date: str
    renew_counter: int
    wireguard_public_key: str
    wireguard_ipv4: str
    wireguard_ipv6: str
    vpn_last_from_unix: int
    vpn_last_from_date: str
    vpn_last_to_unix: int
    vpn_last_to_date: str
    vpn_attempt_unix: int
    vpn_attempt_date: str
    vpn_attempt_message: str
    status: str

class Device:
    """Represents a registered device associated with the account.

    Attributes:
        id: Unique identifier for the device.
        name: Display name of the device.
        description: Description of the device.
        version: Version of the client/software associated with the device.
        renew_first_unix: Unix timestamp of the device's first renewal.
        renew_first_date: Human-readable date of the device's first renewal.
        renew_last_unix: Unix timestamp of the device's most recent renewal.
        renew_last_date: Human-readable date of the device's most recent renewal.
        renew_counter: Number of times the device has been renewed.
        wireguard_public_key: The device's WireGuard public key.
        wireguard_ipv4: IPv4 address assigned to the device over WireGuard.
        wireguard_ipv6: IPv6 address assigned to the device over WireGuard.
        vpn_last_from_unix: Unix timestamp of the start of the device's last VPN session.
        vpn_last_from_date: Human-readable start date of the device's last VPN session.
        vpn_last_to_unix: Unix timestamp of the end of the device's last VPN session.
        vpn_last_to_date: Human-readable end date of the device's last VPN session.
        vpn_attempt_unix: Unix timestamp of the device's last connection attempt.
        vpn_attempt_date: Human-readable date of the device's last connection attempt.
        vpn_attempt_message: Message/result associated with the last connection attempt.
        status: Current status of the device.
    """
    def __init__(self, **kwargs: Unpack[DeviceDict]):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.version = kwargs.get("version")
        self.renew_first_unix = kwargs.get("renew_first_unix")
        self.renew_first_date = kwargs.get("renew_first_date")
        self.renew_last_unix = kwargs.get("renew_last_unix")
        self.renew_last_date = kwargs.get("renew_last_date")
        self.renew_counter = kwargs.get("renew_counter")
        self.wireguard_public_key = kwargs.get("wireguard_public_key")
        self.wireguard_ipv4 = kwargs.get("wireguard_ipv4")
        self.wireguard_ipv6 = kwargs.get("wireguard_ipv6")
        self.vpn_last_from_unix = kwargs.get("vpn_last_from_unix")
        self.vpn_last_from_date = kwargs.get("vpn_last_from_date")
        self.vpn_last_to_unix = kwargs.get("vpn_last_to_unix")
        self.vpn_last_to_date = kwargs.get("vpn_last_to_date")
        self.vpn_attempt_unix = kwargs.get("vpn_attempt_unix")
        self.vpn_attempt_date = kwargs.get("vpn_attempt_date")
        self.vpn_attempt_message = kwargs.get("vpn_attempt_message")
        self.status = kwargs.get("status")
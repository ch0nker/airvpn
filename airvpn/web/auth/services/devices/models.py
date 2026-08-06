from typing import TypedDict, Unpack

class DeviceKeyDict(TypedDict, total=False):
    name: str
    id: str
    description: str | None
    color: str
    version: str
    renew_first_date: int
    renew_last_date: int
    renew_counter: int
    wg_public_key: str
    wg_ipv4: str
    wg_ipv6: str
    show_dns: bool
    vpn_last_from_date: str
    vpn_last_to_date: str
    vpn_attempt_date: str
    vpn_attempt_message: str
    deprecated: bool
    pending: str

class DeviceKey:
    """A device associated with the user's account.

    Represents an entry from the ``keys`` section of the `PortManager`
    manifest. Despite the name, these correspond to the user's devices
    rather than cryptographic keys.

    Attributes:
        name (str): Display name of the device.
        id (str): Unique identifier of the device.
        description (str | None): Optional free-text description of the device.
        color (str): Color label/tag associated with the device.
        version (str): Version string of the device's client software.
        renew_first_date (int): Timestamp of the device's first renewal.
        renew_last_date (int): Timestamp of the device's most recent renewal.
        renew_counter (int): Number of times the device has been renewed.
        wg_public_key (str): WireGuard public key for the device.
        wg_ipv4 (str): WireGuard IPv4 address assigned to the device.
        wg_ipv6 (str): WireGuard IPv6 address assigned to the device.
        show_dns (bool): Whether DNS info is shown for the device.
        vpn_last_from_date (str): Start date of the device's last VPN session.
        vpn_last_to_date (str): End date of the device's last VPN session.
        vpn_attempt_date (str): Date of the device's last connection attempt.
        vpn_attempt_message (str): Message/status from the last connection attempt.
        deprecated (bool): Whether the device is deprecated. Defaults to False.
        pending (str): Pending action or status for the device, if any.
    """
    def __init__(self, **kwargs: Unpack[DeviceKeyDict]):
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.description = kwargs.get("description")
        self.color = kwargs.get("color")
        self.version = kwargs.get("version")
        self.renew_first_date = kwargs.get("renew_first_date")
        self.renew_last_date = kwargs.get("renew_last_date")
        self.renew_counter = kwargs.get("renew_counter")
        self.wg_public_key = kwargs.get("wg_public_key")
        self.wg_ipv4 = kwargs.get("wg_ipv4")
        self.wg_ipv6 = kwargs.get("wg_ipv6")
        self.show_dns = kwargs.get("show_dns")
        self.vpn_last_from_date = kwargs.get("vpn_last_from_date")
        self.vpn_last_to_date = kwargs.get("vpn_last_to_date")
        self.vpn_attempt_date = kwargs.get("vpn_attempt_date")
        self.vpn_attempt_message = kwargs.get("vpn_attempt_message")
        self.deprecated = kwargs.get("deprecated", False)
        self.pending = kwargs.get("pending")

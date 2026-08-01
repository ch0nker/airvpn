from typing import TypedDict, Literal, Unpack
from datetime import datetime, timezone
from enum import IntEnum

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

class APIKeyDict(TypedDict, total=False):
    id: str
    color: str
    name: str
    secret_short: str
    secret: str
    creation_date: int

class APIKey:
    """An AirVPN API key belonging to the authenticated user.

    Constructed from the key entries returned by the `APIManager`
    manifest.

    Attributes:
        id (str | None): Unique identifier of the key.
        color (str | None): CSS color assigned to the key for display
            purposes, as an HSL string (e.g. ``"hsl(68,80%,87.5%)"``).
        name (str | None): Display name of the key.
        secret_short (str | None): Truncated/masked preview of the key's
            secret, safe for display.
        secret (str | None): The key's full secret value.
        creation_date (datetime): UTC timestamp of when the key was
            created, converted from the manifest's Unix timestamp.
    """
    def __init__(self, **kwargs: Unpack[APIKeyDict]):
        self.id = kwargs.get("id")
        self.color = kwargs.get("color")
        self.name = kwargs.get("name")
        self.secret_short = kwargs.get("secret_short")
        self.secret = kwargs.get("secret")
        self.creation_date = datetime.fromtimestamp(kwargs.get("creation_date"), tz=timezone.utc)

class PortKey:
    """A device associated with the user's account.

    Represents an entry from the ``keys`` section of the `PortManager`
    manifest. Despite the name, these correspond to the user's devices
    rather than cryptographic keys.

    Attributes:
        name (str): Display name of the device.
        id (str): Unique identifier of the device.
    """
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

class PortDict(TypedDict, total=False):
    port: int
    pool: int
    notes: str | None
    enabled: bool
    device: str
    protocol: Literal["both", "tcp", "udp"]
    iplayer: Literal["both", "v6", "v4"]
    local: int
    dns: str

class Port:
    """A single forwarded port owned by the authenticated user.

    Constructed from the port entries returned by the `PortManager`
    manifest, and from the responses of port-mutating actions like
    `PortManager.open`.

    Attributes:
        port (int | None): The forwarded port number.
        pool (int | None): Identifier of the pool the port belongs to.
        notes (str | None): Free-text note/description attached to the port.
        device (str | None): Name of the device associated with the port.
        enabled (bool | None): Whether the port is currently enabled.
        protocol (Literal["both", "tcp", "udp"] | None): Protocol
            restriction for the port.
        iplayer (Literal["both", "v6", "v4"] | None): IP layer restriction
            for the port.
        local (int | None): Local port the forwarded port maps to.
        dns (str | None): Dynamic DNS hostname associated with the port.
    """
    def __init__(self, **kwargs: Unpack[PortDict]):
        self.port = kwargs.get("port")
        self.pool = kwargs.get("pool")
        self.notes = kwargs.get("notes")
        self.device = kwargs.get("device")
        self.enabled = kwargs.get("enabled")
        self.protocol = kwargs.get("protocol")
        self.iplayer = kwargs.get("iplayer")
        self.local = kwargs.get("local")
        self.dns = kwargs.get("dns")


class PortSessionDict(TypedDict, total=False):
    port: int
    pool: int
    dns_name: str
    notes: str
    local: int
    iplayer: Literal["both", "v6", "v4"]
    protocol: Literal["both", "tcp", "udp"]
    server_name: str
    server_planet: str
    server_continent: str
    server_location: str
    server_country: str
    device_name: str
    device_description: str
    server_ip: str
    client_ip: str

class PortSession:
    """An active session using one of the user's forwarded ports.

    Constructed from the session entries returned by
    `PortManager.get_sessions`, and used by `PortManager.test_open` to
    check connectivity.

    Attributes:
        port (int | None): The forwarded port number the session is using.
        pool (int | None): Identifier of the pool the port belongs to.
        dns_name (str | None): Dynamic DNS hostname associated with the port.
        notes (str | None): Free-text note/description attached to the port.
        local (int | None): Local port the forwarded port maps to.
        iplayer (Literal["both", "v6", "v4"] | None): IP layer restriction
            for the port.
        protocol (Literal["both", "tcp", "udp"] | None): Protocol used by
            the session.
        server_name (str | None): Name of the VPN server handling the
            session.
        server_planet (str | None): Planet designation of the VPN server
            (AirVPN's naming scheme for servers).
        server_continent (str | None): Continent the VPN server is located
            on.
        server_location (str | None): City/location of the VPN server.
        server_country (str | None): Country the VPN server is located in.
        device_name (str | None): Name of the device that opened the
            session.
        device_description (str | None): Description of the device that
            opened the session.
        server_ip (str | None): IP address of the VPN server.
        client_ip (str | None): IP address of the connecting client.
    """
    def __init__(self, **kwargs: Unpack[PortSessionDict]):
        self.port = kwargs.get("port")
        self.pool = kwargs.get("pool")
        self.dns_name = kwargs.get("dns_name")
        self.notes = kwargs.get("notes")
        self.local = kwargs.get("local")
        self.iplayer = kwargs.get("iplayer")
        self.protocol = kwargs.get("protocol")
        self.server_name = kwargs.get("server_name")
        self.server_planet = kwargs.get("server_planet")
        self.server_continent = kwargs.get("server_continent")
        self.server_location = kwargs.get("server_location")
        self.server_country = kwargs.get("server_country")
        self.device_name = kwargs.get("device_name")
        self.device_description = kwargs.get("device_description")
        self.server_ip = kwargs.get("server_ip")
        self.client_ip = kwargs.get("client_ip")

class ProfilePrivacy(IntEnum):
    """Controls who is allowed to view a user's profile.

    Used with `AuthUser.edit_profile` to set the
    `air_ipb_profile_privacy_title` field on the profile edit form.

    Attributes:
        ALL: Profile is visible to everyone, including guests.
        FOLLOWED_MEMBERS: Profile is visible only to members the user follows.
        COMMUNITY_MEMBERS: Profile is visible only to registered/logged-in
            community members.
        PRIVATE: Profile is visible only to the user themselves.
    """
    ALL = 1
    FOLLOWED_MEMBERS = 2
    COMMUNITY_MEMBERS = 3
    PRIVATE = 4
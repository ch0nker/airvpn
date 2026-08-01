from typing import TypedDict, Literal, Unpack
from enum import IntEnum

class Key:
    """A key associated with the user's port pool.

    Represents an entry from the ``keys`` section of the `PortManager`
    manifest.

    Attributes:
        name (str): Display name of the key.
        id (str): Unique identifier of the key.
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


class SessionDict(TypedDict, total=False):
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

class Session:
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
    def __init__(self, **kwargs: Unpack[SessionDict]):
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
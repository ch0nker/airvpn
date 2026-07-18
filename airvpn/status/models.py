from typing import Unpack, TypedDict
from airvpn.network import Status

class ServerDict(TypedDict, total=False):
    public_name: str
    country_name: str
    country_code: str
    location: str
    continent: str
    bw: int
    bw_max: int
    users: int
    currentload: int
    ip_v4_in1: str
    ip_v4_in2: str
    ip_v4_in3: str
    ip_v4_in4: str
    ip_v6_in1: str
    ip_v6_in2: str
    ip_v6_in3: str
    ip_v6_in4: str
    health: str
    warning: str | None

class Server:
    """Represents a single VPN server and its current status.

    Attributes:
        public_name: The server's public display name.
        country_name: Country where the server is located.
        country_code: ISO country code of the server's location.
        location: Specific city/region of the server.
        continent: Continent where the server is located.
        bw: Bandwidth currently in use, in Mbit/s.
        bw_max: Maximum bandwidth available, in Mbit/s.
        users: Number of users currently connected to the server.
        currentload: Current load as a percentage.
        ip_v4_in1: First IPv4 address for incoming connections.
        ip_v4_in2: Second IPv4 address for incoming connections.
        ip_v4_in3: Third IPv4 address for incoming connections.
        ip_v4_in4: Fourth IPv4 address for incoming connections.
        ip_v6_in1: First IPv6 address for incoming connections.
        ip_v6_in2: Second IPv6 address for incoming connections.
        ip_v6_in3: Third IPv6 address for incoming connections.
        ip_v6_in4: Fourth IPv6 address for incoming connections.
        health: Server health status (ok, warning, or error). A server
            in error status does not accept connections.
        warning: Reason for a non-ok health status. Only present when
            health is warning or error; otherwise None.
    """
    def __init__(self, **kwargs: Unpack[ServerDict]):
        self.public_name = kwargs.get("public_name")
        self.country_name = kwargs.get("country_name")
        self.country_code = kwargs.get("country_code")
        self.location = kwargs.get("location")
        self.continent = kwargs.get("continent")
        self.bw = kwargs.get("bw")
        self.bw_max = kwargs.get("bw_max")
        self.users = kwargs.get("users")
        self.currentload = kwargs.get("currentload")
        self.ip_v4_in1 = kwargs.get("ip_v4_in1")
        self.ip_v4_in2 = kwargs.get("ip_v4_in2")
        self.ip_v4_in3 = kwargs.get("ip_v4_in3")
        self.ip_v4_in4 = kwargs.get("ip_v4_in4")
        self.ip_v6_in1 = kwargs.get("ip_v6_in1")
        self.ip_v6_in2 = kwargs.get("ip_v6_in2")
        self.ip_v6_in3 = kwargs.get("ip_v6_in3")
        self.ip_v6_in4 = kwargs.get("ip_v6_in4")
        self.health = Status(kwargs.get("health"))
        self.warning = kwargs.get("warning")

class RoutingDict(TypedDict, total=False):
    public_name: str
    country_name: str
    country_code: str
    location: str
    continent: str
    bw: int
    bw_max: int
    currentload: int
    health: str
    warning: str | None

class Routing:
    """Represents a routing node's status (no user/IP data attached).

    Attributes:
        public_name: The node's public display name.
        country_name: Country where the node is located.
        country_code: ISO country code of the node's location.
        location: Specific city/region of the node.
        continent: Continent where the node is located.
        bw: Bandwidth currently in use, in Mbit/s.
        bw_max: Maximum bandwidth available, in Mbit/s.
        currentload: Current load as a percentage.
        health: Node health status (ok, warning, or error). A node
            in error status does not accept connections.
        warning: Reason for a non-ok health status. Only present when
            health is warning or error; otherwise None.
    """
    def __init__(self, **kwargs: Unpack[RoutingDict]):
        self.public_name = kwargs.get("public_name")
        self.country_name = kwargs.get("country_name")
        self.country_code = kwargs.get("country_code")
        self.location = kwargs.get("location")
        self.continent = kwargs.get("continent")
        self.bw = kwargs.get("bw")
        self.bw_max = kwargs.get("bw_max")
        self.currentload = kwargs.get("currentload")
        self.health = Status(kwargs.get("health"))
        self.warning = kwargs.get("warning")

class CountryDict(TypedDict, total=False):
    country_name: str
    country_code: str
    server_best: str
    bw: int
    bw_max: int
    users: int
    servers: int
    currentload: int
    ip_v4_in1: str
    ip_v4_in2: str
    ip_v4_in3: str
    ip_v4_in4: str
    ip_v6_in1: str
    ip_v6_in2: str
    ip_v6_in3: str
    ip_v6_in4: str
    health: str
    warning: str | None

class Country:
    """Represents aggregate VPN status for a country.

    Attributes:
        country_name: The country's name.
        country_code: ISO country code.
        server_best: The recommended server for this country.
        bw: Bandwidth currently in use across the country, in Mbit/s.
        bw_max: Maximum bandwidth available across the country, in Mbit/s.
        users: Number of users currently connected in this country.
        servers: Number of servers available in this country.
        currentload: Current load as a percentage.
        ip_v4_in1: First IPv4 hostname for incoming connections.
        ip_v4_in2: Second IPv4 hostname for incoming connections.
        ip_v4_in3: Third IPv4 hostname for incoming connections.
        ip_v4_in4: Fourth IPv4 hostname for incoming connections.
        ip_v6_in1: First IPv6 hostname for incoming connections.
        ip_v6_in2: Second IPv6 hostname for incoming connections.
        ip_v6_in3: Third IPv6 hostname for incoming connections.
        ip_v6_in4: Fourth IPv6 hostname for incoming connections.
        health: Aggregate health status (ok, warning, or error). A
            country in error status does not accept connections.
        warning: Reason for a non-ok health status. Only present when
            health is warning or error; otherwise None.
    """
    def __init__(self, **kwargs: Unpack[CountryDict]):
        self.country_name = kwargs.get("country_name")
        self.country_code = kwargs.get("country_code")
        self.server_best = kwargs.get("server_best")
        self.bw = kwargs.get("bw")
        self.bw_max = kwargs.get("bw_max")
        self.users = kwargs.get("users")
        self.servers = kwargs.get("servers")
        self.currentload = kwargs.get("currentload")
        self.ip_v4_in1 = kwargs.get("ip_v4_in1")
        self.ip_v4_in2 = kwargs.get("ip_v4_in2")
        self.ip_v4_in3 = kwargs.get("ip_v4_in3")
        self.ip_v4_in4 = kwargs.get("ip_v4_in4")
        self.ip_v6_in1 = kwargs.get("ip_v6_in1")
        self.ip_v6_in2 = kwargs.get("ip_v6_in2")
        self.ip_v6_in3 = kwargs.get("ip_v6_in3")
        self.ip_v6_in4 = kwargs.get("ip_v6_in4")
        self.health = Status(kwargs.get("health"))
        self.warning = kwargs.get("warning")

class ContinentDict(TypedDict, total=False):
    public_name: str
    server_best: str
    bw: int
    bw_max: int
    users: int
    servers: int
    currentload: int
    ip_v4_in1: str
    ip_v4_in2: str
    ip_v4_in3: str
    ip_v4_in4: str
    ip_v6_in1: str
    ip_v6_in2: str
    ip_v6_in3: str
    ip_v6_in4: str
    health: str
    warning: str | None

class Continent:
    """Represents aggregate VPN status for a continent.

    Attributes:
        public_name: The continent's display name.
        server_best: The recommended server for this continent.
        bw: Bandwidth currently in use across the continent, in Mbit/s.
        bw_max: Maximum bandwidth available across the continent, in Mbit/s.
        users: Number of users currently connected in this continent.
        servers: Number of servers available in this continent.
        currentload: Current load as a percentage.
        ip_v4_in1: First IPv4 hostname for incoming connections.
        ip_v4_in2: Second IPv4 hostname for incoming connections.
        ip_v4_in3: Third IPv4 hostname for incoming connections.
        ip_v4_in4: Fourth IPv4 hostname for incoming connections.
        ip_v6_in1: First IPv6 hostname for incoming connections.
        ip_v6_in2: Second IPv6 hostname for incoming connections.
        ip_v6_in3: Third IPv6 hostname for incoming connections.
        ip_v6_in4: Fourth IPv6 hostname for incoming connections.
        health: Aggregate health status (ok, warning, or error). A
            continent in error status does not accept connections.
        warning: Reason for a non-ok health status. Only present when
            health is warning or error; otherwise None.
    """
    def __init__(self, **kwargs: Unpack[ContinentDict]):
        self.public_name = kwargs.get("public_name")
        self.server_best = kwargs.get("server_best")
        self.bw = kwargs.get("bw")
        self.bw_max = kwargs.get("bw_max")
        self.users = kwargs.get("users")
        self.servers = kwargs.get("servers")
        self.currentload = kwargs.get("currentload")
        self.ip_v4_in1 = kwargs.get("ip_v4_in1")
        self.ip_v4_in2 = kwargs.get("ip_v4_in2")
        self.ip_v4_in3 = kwargs.get("ip_v4_in3")
        self.ip_v4_in4 = kwargs.get("ip_v4_in4")
        self.ip_v6_in1 = kwargs.get("ip_v6_in1")
        self.ip_v6_in2 = kwargs.get("ip_v6_in2")
        self.ip_v6_in3 = kwargs.get("ip_v6_in3")
        self.ip_v6_in4 = kwargs.get("ip_v6_in4")
        self.health = Status(kwargs.get("health"))
        self.warning = kwargs.get("warning")

class PlanetDict(TypedDict, total=False):
    public_name: str
    server_best: str
    bw: int
    bw_max: int
    users: int
    servers: int
    currentload: int
    ip_v4_in1: str
    ip_v4_in2: str
    ip_v4_in3: str
    ip_v4_in4: str
    ip_v6_in1: str
    ip_v6_in2: str
    ip_v6_in3: str
    ip_v6_in4: str
    health: str
    warning: str | None


class Planet:
    """Represents aggregate VPN status for the whole planet (global stats).

    Attributes:
        public_name: The planet's display name.
        server_best: The recommended server globally.
        bw: Bandwidth currently in use globally, in Mbit/s.
        bw_max: Maximum bandwidth available globally, in Mbit/s.
        users: Number of users currently connected globally.
        servers: Number of servers available globally.
        currentload: Current load as a percentage.
        ip_v4_in1: First IPv4 hostname for incoming connections.
        ip_v4_in2: Second IPv4 hostname for incoming connections.
        ip_v4_in3: Third IPv4 hostname for incoming connections.
        ip_v4_in4: Fourth IPv4 hostname for incoming connections.
        ip_v6_in1: First IPv6 hostname for incoming connections.
        ip_v6_in2: Second IPv6 hostname for incoming connections.
        ip_v6_in3: Third IPv6 hostname for incoming connections.
        ip_v6_in4: Fourth IPv6 hostname for incoming connections.
        health: Aggregate health status (ok, warning, or error). A
            planet-level entry in error status does not accept connections.
        warning: Reason for a non-ok health status. Only present when
            health is warning or error; otherwise None.
    """
    def __init__(self, **kwargs: Unpack[PlanetDict]):
        self.public_name = kwargs.get("public_name")
        self.server_best = kwargs.get("server_best")
        self.bw = kwargs.get("bw")
        self.bw_max = kwargs.get("bw_max")
        self.users = kwargs.get("users")
        self.servers = kwargs.get("servers")
        self.currentload = kwargs.get("currentload")
        self.ip_v4_in1 = kwargs.get("ip_v4_in1")
        self.ip_v4_in2 = kwargs.get("ip_v4_in2")
        self.ip_v4_in3 = kwargs.get("ip_v4_in3")
        self.ip_v4_in4 = kwargs.get("ip_v4_in4")
        self.ip_v6_in1 = kwargs.get("ip_v6_in1")
        self.ip_v6_in2 = kwargs.get("ip_v6_in2")
        self.ip_v6_in3 = kwargs.get("ip_v6_in3")
        self.ip_v6_in4 = kwargs.get("ip_v6_in4")
        self.health = Status(kwargs.get("health"))
        self.warning = kwargs.get("warning")
from typing import Unpack, TypedDict

class ConnectionDict(TypedDict):
    device_name: str
    device_description: str | None
    vpn_ip: str
    vpn_ipv4: str
    vpn_ipv6: str
    exit_ip: str
    exit_ipv4: str
    exit_ipv6: str
    server_name: str
    server_country: str
    server_country_code: str
    server_continent: str
    server_location: str
    server_bw: int
    bytes_read: int
    bytes_write: int
    connected_since_date: str
    connected_since_unix: int
    speed_read: int
    speed_write: int

class Connection:
    """Connection class for the userinfo endpoint.

    Attributes:
        device_name: Name of the connected device.
        device_description: Description of the connected device.
        vpn_ip: VPN-assigned IP address.
        vpn_ipv4: VPN-assigned IPv4 address.
        vpn_ipv6: VPN-assigned IPv6 address.
        exit_ip: Exit node IP address.
        exit_ipv4: Exit node IPv4 address.
        exit_ipv6: Exit node IPv6 address.
        server_name: Name of the connected server.
        server_country: Country where the server is located.
        server_country_code: ISO country code of the server's location.
        server_continent: Continent where the server is located.
        server_location: Specific location/city of the server.
        server_bw: Server bandwidth.
        bytes_read: Total bytes received during this connection.
        bytes_write: Total bytes sent during this connection.
        connected_since_date: Human-readable timestamp of when the connection started.
        connected_since_unix: Unix timestamp of when the connection started.
        speed_read: Current/average download speed.
        speed_write: Current/average upload speed.
    """
    def __init__(self, **kwargs: Unpack[ConnectionDict]):
        self.device_name = kwargs.get("device_name")
        self.device_description = kwargs.get("device_description")
        self.vpn_ip = kwargs.get("vpn_ip")
        self.vpn_ipv4 = kwargs.get("vpn_ipv4")
        self.vpn_ipv6 = kwargs.get("vpn_ipv6")
        self.exit_ip = kwargs.get("exit_ip")
        self.exit_ipv4 = kwargs.get("exit_ipv4")
        self.exit_ipv6 = kwargs.get("exit_ipv6")
        self.server_name = kwargs.get("server_name")
        self.server_country = kwargs.get("server_country")
        self.server_country_code = kwargs.get("server_country_code")
        self.server_continent = kwargs.get("server_continent")
        self.server_location = kwargs.get("server_location")
        self.server_bw = kwargs.get("server_bw")
        self.bytes_read = kwargs.get("bytes_read")
        self.bytes_write = kwargs.get("bytes_write")
        self.connected_since_date = kwargs.get("connected_since_date")
        self.connected_since_unix = kwargs.get("connected_since_unix")
        self.speed_read = kwargs.get("speed_read")
        self.speed_write = kwargs.get("speed_write")

class UserDict(TypedDict):
    login: str
    premium: bool
    expiration_days: int
    pool: int
    posts: int
    last_post: int
    register_unix: int
    register_date: str
    expiration_unix: int
    expiration_date: str
    last_visit_unix: int
    last_visit_date: str
    last_activity_unix: int
    last_activity_date: str
    credits: int
    last_attempt_unix: int
    last_attempt_date: str
    credit: list
    connected: bool

class User:
    """User class for the userinfo endpoint.

    Attributes:
        login: The account's username.
        premium: Whether the account has an active premium subscription.
        expiration_days: Days remaining until premium expires.
        pool: Unknown.
        posts: Total number of posts made by the account.
        last_post: Unknown.
        register_unix: Unix timestamp of account registration.
        register_date: Human-readable registration date.
        expiration_unix: Unix timestamp of when premium expires.
        expiration_date: Human-readable premium expiration date.
        last_visit_unix: Unix timestamp of the account's last site visit.
        last_visit_date: Human-readable date of the last site visit.
        last_activity_unix: Unix timestamp of the account's last recorded activity.
        last_activity_date: Human-readable date of the last recorded activity.
        credits: Current credit balance.
        last_attempt_unix: Unix timestamp of the last login attempt.
        last_attempt_date: Human-readable date of the last login attempt.
        credit: Unknown.
        connected: Whether the account is currently connected/online.
    """
    def __init__(self, **kwargs: Unpack[UserDict]):
        self.login = kwargs.get("login")
        self.premium = kwargs.get("premium")
        self.expiration_days = kwargs.get("expiration_days")
        self.pool = kwargs.get("pool")
        self.posts = kwargs.get("posts")
        self.last_post = kwargs.get("last_post")
        self.register_unix = kwargs.get("register_unix")
        self.register_date = kwargs.get("register_date")
        self.expiration_unix = kwargs.get("expiration_unix")
        self.expiration_date = kwargs.get("expiration_date")
        self.last_visit_unix = kwargs.get("last_visit_unix")
        self.last_visit_date = kwargs.get("last_visit_date")
        self.last_activity_unix = kwargs.get("last_activity_unix")
        self.last_activity_date = kwargs.get("last_activity_date")
        self.credits = kwargs.get("credits")
        self.last_attempt_unix = kwargs.get("last_attempt_unix")
        self.last_attempt_date = kwargs.get("last_attempt_date")
        self.credit = kwargs.get("credit", [])
        self.connected = kwargs.get("connected")
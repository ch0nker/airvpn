from __future__ import annotations

from typing import TypedDict, Unpack

from xml.etree import ElementTree


def _int(value: str | None) -> int | None:
    """Convert a string to an int, passing `None` through unchanged.

    Args:
        value: The string to convert, or `None`.

    Returns:
        The parsed `int`, or `None` if `value` was `None`.
    """
    return int(value) if value is not None else None

def _csv(value: str | None) -> list[str]:
    """Split a comma-separated string into a list of strings.

    Args:
        value: The comma-separated string to split, or `None`.

    Returns:
        A list of the split values, or an empty list if `value` was `None` or empty.
    """
    return value.split(",") if value else []

class KeyDict(TypedDict, total=False):
    mame: str
    crt: str
    key: str
    wg_private_key: str
    wg_preshared: str
    wg_ipv4: str
    wg_ipv6: str
    wg_dns_ipv4: str
    wg_dns_ipv6: str


class Key:
    """Represents a device's certificates/keys issued to a user's account.

    Attributes:
        name: The device/key's name.
        crt: The device's OpenVPN certificate.
        key: The device's OpenVPN private key.
        wg_private_key: The device's WireGuard private key.
        wg_preshared: The device's WireGuard preshared key.
        wg_ipv4: The device's assigned WireGuard IPv4 address.
        wg_ipv6: The device's assigned WireGuard IPv6 address.
        wg_dns_ipv4: The IPv4 DNS server to use for this device's WireGuard connection.
        wg_dns_ipv6: The IPv6 DNS server to use for this device's WireGuard connection.
    """
    def __init__(self, **kwargs: Unpack[KeyDict]):
        self.name = kwargs.get("name")
        self.crt = kwargs.get("crt")
        self.key = kwargs.get("key")
        self.wg_private_key = kwargs.get("wg_private_key")
        self.wg_preshared = kwargs.get("wg_preshared")
        self.wg_ipv4 = kwargs.get("wg_ipv4")
        self.wg_ipv6 = kwargs.get("wg_ipv6")
        self.wg_dns_ipv4 = kwargs.get("wg_dns_ipv4")
        self.wg_dns_ipv6 = kwargs.get("wg_dns_ipv6")

    @classmethod
    def from_element(cls, element: ElementTree.Element) -> Key:
        """Parses a `<key>` XML element into a `Key`.

        Args:
            element: The `<key>` element.

        Returns:
            A populated `Key` instance.
        """
        return cls(
            name=element.get("name"),
            crt=element.get("crt"),
            key=element.get("key"),
            wg_private_key=element.get("wg_private_key"),
            wg_preshared=element.get("wg_preshared"),
            wg_ipv4=element.get("wg_ipv4"),
            wg_ipv6=element.get("wg_ipv6"),
            wg_dns_ipv4=element.get("wg_dns_ipv4"),
            wg_dns_ipv6=element.get("wg_dns_ipv6")
        )
    
class UserDict(TypedDict, total=False):
    ts: int
    login: str
    expirationdate: str
    ca: str
    ta: str
    tls_crypt: str
    ssh_key: str
    ssh_ppk: str
    ssl_crt: str
    wg_public_key: str
    keys: list[Key]
    message: str
    message_action: str

class User:
    """Represents the authenticated account and its connection credentials.

    This is the parsed form of the response from `AirClient.login()`.

    Attributes:
        ts: Unix timestamp the response was generated.
        login: The account's username.
        expiration_date: The account's expiration date.
        ca: The OpenVPN CA certificate.
        ta: The OpenVPN TLS-auth key.
        tls_crypt: The OpenVPN tls-crypt key.
        ssh_key: The SSH tunnel private key.
        ssh_ppk: The SSH tunnel private key in PPK format.
        ssl_crt: The SSL/stunnel certificate.
        wg_public_key: The server's WireGuard public key.
        keys: The devices/keys registered to this account.
        message: A message from the server, if any (e.g. describing a login failure).
        message_action: The action associated with `message`, e.g. `"stop"` when login fails.
    """
    def __init__(self, **kwargs: Unpack[UserDict]):
        self.ts = kwargs.get("ts")
        self.login = kwargs.get("login")
        self.expiration_date = kwargs.get("expirationdate")
        self.ca = kwargs.get("ca")
        self.ta = kwargs.get("ta")
        self.tls_crypt = kwargs.get("tls_crypt")
        self.ssh_key = kwargs.get("ssh_key")
        self.ssh_ppk = kwargs.get("ssh_ppk")
        self.ssl_crt = kwargs.get("ssl_crt")
        self.wg_public_key = kwargs.get("wg_public_key")
        self.keys = kwargs.get("keys", [])
        self.message = kwargs.get("message")
        self.message_action = kwargs.get("message_action")

    @classmethod
    def from_element(cls, element: ElementTree.Element) -> User:
        """Parses a `<user>` XML element into a `User`.

        Args:
            element: The `<user>` element.

        Returns:
            A populated `User` instance.
        """
        return cls(**element.attrib)

    @classmethod
    def from_string(cls, xml: str) -> User:
        """Parses an XML string into a `User`.

        Args:
            xml: The decrypted XML response string, as returned by `AirClient.request()`.

        Returns:
            A populated `User` instance.
        """
        return cls.from_element(ElementTree.fromstring(xml))

class ManifestUrlDict(TypedDict, total=False):
    address: str

class ManifestUrl:
    """A bootstrap server URL for AirClient's legacy protocol.

    Attributes:
        address: The bootstrap server's URL.
    """
    def __init__(self, **kwargs: Unpack[ManifestUrlDict]):
        self.address = kwargs.get("address")

    def __str__(self):
        """Returns the bootstrap server's URL."""
        return self.address


class ModeDict(TypedDict, total=False):
    title: str
    protocol: str
    port: int
    entry_index: int
    specs: str | None
    type: str
    openvpn_minversion: str | None
    openvpn_directives: str | None
    ssh_destination: int

class Mode:
    """A connection mode offered by a server (a protocol/port/type combination).

    Attributes:
        title: Human-readable description of the mode.
        protocol: Transport protocol (e.g. "udp", "tcp", "ssh", "ssl").
        port: Port number to connect to.
        entry_index: Index into a server's `ips_entry` list to use for this mode.
        specs: Extra TLS/connection specs (e.g. "tls-crypt, tls1.2"), if any.
        type: VPN type for this mode (e.g. "wireguard", "openvpn").
        openvpn_minversion: Minimum required OpenVPN version, if applicable.
        openvpn_directives: Extra OpenVPN config directives specific to this mode, if any.
        ssh_destination: SSH tunnel destination port, or 0 if not applicable.
    """
    def __init__(self, **kwargs: Unpack[ModeDict]):
        self.title = kwargs.get("title")
        self.protocol = kwargs.get("protocol")
        self.port = kwargs.get("port")
        self.entry_index = kwargs.get("entry_index")
        self.specs = kwargs.get("specs") or None
        self.type = kwargs.get("type")
        self.openvpn_minversion = kwargs.get("openvpn_minversion") or None
        self.openvpn_directives = kwargs.get("openvpn_directives") or None
        self.ssh_destination = kwargs.get("ssh_destination")


class RSAParametersDict(TypedDict, total=False):
    exponent: str
    modulus: str

class RSAParameters:
    """The RSA public key used to encrypt requests to the bootstrap servers.

    Attributes:
        exponent: Base64-encoded RSA public key exponent.
        modulus: Base64-encoded RSA public key modulus.
    """
    def __init__(self, **kwargs: Unpack[RSAParametersDict]):
        self.exponent = kwargs.get("exponent")
        self.modulus = kwargs.get("modulus")


class ManifestServerDict(TypedDict, total=False):
    name: str
    country_code: str
    location: str
    bw_max: int
    bw: int
    users: int
    users_max: int
    ips_entry: list[str]
    ips_exit: list[str]
    scorebase: int
    set: int | None
    group: int
    openvpn_directives: str | None
    warning_open: str | None
    warning_closed: str | None

class ManifestServer:
    """A single VPN server entry from the manifest.

    Attributes:
        name: The server's public name.
        country_code: ISO country code of the server's location.
        location: City/region of the server.
        bw_max: Maximum bandwidth available, in Mbit/s.
        bw: Bandwidth currently in use, in bytes.
        users: Number of users currently connected.
        users_max: Maximum number of users this server accepts.
        ips_entry: Entry IP addresses (IPv4 and IPv6), indexed by a mode's `entry_index`.
        ips_exit: Exit IP addresses (IPv4 and IPv6) traffic appears to originate from.
        scorebase: Base score used in server selection/ranking.
        set: Server set identifier, if applicable.
        group: Server group identifier, matches a `ServersGroup.group`.
        openvpn_directives: Extra server-specific OpenVPN config directives, if any.
        warning_open: A warning shown for an otherwise-open server (e.g. elevated packet loss), if any.
        warning_closed: Reason the server is closed/unavailable (e.g. maintenance), if any.
    """
    def __init__(self, **kwargs: Unpack[ManifestServerDict]):
        self.name = kwargs.get("name")
        self.country_code = kwargs.get("country_code")
        self.location = kwargs.get("location")
        self.bw_max = kwargs.get("bw_max")
        self.bw = kwargs.get("bw")
        self.users = kwargs.get("users")
        self.users_max = kwargs.get("users_max")
        self.ips_entry = kwargs.get("ips_entry") or []
        self.ips_exit = kwargs.get("ips_exit") or []
        self.scorebase = kwargs.get("scorebase")
        self.set = kwargs.get("set")
        self.group = kwargs.get("group")
        self.openvpn_directives = kwargs.get("openvpn_directives") or None
        self.warning_open = kwargs.get("warning_open") or None
        self.warning_closed = kwargs.get("warning_closed") or None

    @property
    def is_closed(self) -> bool:
        """Whether the server is currently marked unavailable (e.g. for maintenance)."""
        return self.warning_closed is not None

    def __str__(self):
        """Returns the server's public name."""
        return self.name


class ServersGroupDict(TypedDict, total=False):
    support_ipv4: bool
    support_ipv6: bool
    support_check: bool
    ciphers_tls: str
    ciphers_tlssuites: str
    ciphers_data: str
    group: int

class ServersGroup:
    """Shared connection capabilities for a group of servers.

    Attributes:
        support_ipv4: Whether servers in this group support IPv4.
        support_ipv6: Whether servers in this group support IPv6.
        support_check: Whether servers in this group support connectivity checks.
        ciphers_tls: Colon-separated list of supported TLS key-exchange ciphers.
        ciphers_tlssuites: Colon-separated list of supported TLS 1.3 cipher suites.
        ciphers_data: Colon-separated list of supported data-channel ciphers.
        group: The server group identifier these settings apply to.
    """
    def __init__(self, **kwargs: Unpack[ServersGroupDict]):
        self.support_ipv4 = kwargs.get("support_ipv4")
        self.support_ipv6 = kwargs.get("support_ipv6")
        self.support_check = kwargs.get("support_check")
        self.ciphers_tls = kwargs.get("ciphers_tls")
        self.ciphers_tlssuites = kwargs.get("ciphers_tlssuites")
        self.ciphers_data = kwargs.get("ciphers_data")
        self.group = kwargs.get("group")


class ManifestDict(TypedDict, total=False):
    time: int
    next: int
    next_update: int
    dnscheck_host: str
    dnscheck_res1: str
    dnscheck_res2: str
    speed_factor: int
    latency_factor: int
    penality_factor: int
    users_factor: int
    load_factor: int
    ping_factor: int
    pinger_delay: int
    pinger_retry: int
    check_domain: str
    check_dns_query: str
    check_protocol: str
    force_reauth_ts: int
    openvpn_directives: str
    mode_protocol: str
    mode_port: int
    mode_alt: int
    messages: list[str]
    urls: list[ManifestUrl]
    modes: list[Mode]
    rsa: RSAParameters | None
    servers: list[ManifestServer]
    servers_groups: list[ServersGroup]

class Manifest:
    """The AirVPN bootstrap manifest: server list, connection modes, and client configuration.

    This is the parsed form of the response from `AirClient.manifest()`.

    Attributes:
        time: Unix timestamp this manifest was generated.
        next: Unix timestamp the next manifest update is expected.
        next_update: Number of seconds until the next expected update.
        dnscheck_host: Hostname used for DNS-based connectivity checks.
        dnscheck_res1: Expected DNS check response IP, primary.
        dnscheck_res2: Expected DNS check response IP, secondary.
        speed_factor: Weight given to speed in server scoring.
        latency_factor: Weight given to latency in server scoring.
        penality_factor: Weight given to penalties in server scoring.
        users_factor: Weight given to user count in server scoring.
        load_factor: Weight given to load in server scoring.
        ping_factor: Weight given to ping in server scoring.
        pinger_delay: Delay in seconds between pinger runs.
        pinger_retry: Number of pinger retries.
        check_domain: Domain used for connectivity checks.
        check_dns_query: DNS query template used for connectivity checks.
        check_protocol: Protocol used for connectivity checks (e.g. "https").
        force_reauth_ts: Unix timestamp after which reauthentication is forced.
        openvpn_directives: Default OpenVPN config directives applied across modes.
        mode_protocol: Default transport protocol for connections.
        mode_port: Default port for connections.
        mode_alt: Alternate mode indicator.
        messages: Operator messages/announcements included in the manifest.
        urls: Bootstrap server URLs.
        modes: Connection modes available (protocol/port/type combinations).
        rsa: The RSA public key used to encrypt requests, if present.
        servers: Every VPN server known to the manifest.
        servers_groups: Shared connection capabilities, keyed by server group.
    """
    def __init__(self, **kwargs: Unpack[ManifestDict]):
        self.time = kwargs.get("time")
        self.next = kwargs.get("next")
        self.next_update = kwargs.get("next_update")
        self.dnscheck_host = kwargs.get("dnscheck_host")
        self.dnscheck_res1 = kwargs.get("dnscheck_res1")
        self.dnscheck_res2 = kwargs.get("dnscheck_res2")
        self.speed_factor = kwargs.get("speed_factor")
        self.latency_factor = kwargs.get("latency_factor")
        self.penality_factor = kwargs.get("penality_factor")
        self.users_factor = kwargs.get("users_factor")
        self.load_factor = kwargs.get("load_factor")
        self.ping_factor = kwargs.get("ping_factor")
        self.pinger_delay = kwargs.get("pinger_delay")
        self.pinger_retry = kwargs.get("pinger_retry")
        self.check_domain = kwargs.get("check_domain")
        self.check_dns_query = kwargs.get("check_dns_query")
        self.check_protocol = kwargs.get("check_protocol")
        self.force_reauth_ts = kwargs.get("force_reauth_ts")
        self.openvpn_directives = kwargs.get("openvpn_directives")
        self.mode_protocol = kwargs.get("mode_protocol")
        self.mode_port = kwargs.get("mode_port")
        self.mode_alt = kwargs.get("mode_alt")
        self.messages = kwargs.get("messages") or []
        self.urls = kwargs.get("urls") or []
        self.modes = kwargs.get("modes") or []
        self.rsa = kwargs.get("rsa")
        self.servers = kwargs.get("servers") or []
        self.servers_groups = kwargs.get("servers_groups") or []

    @classmethod
    def from_element(cls, element: ElementTree.Element) -> Manifest:
        """Parses a `<manifest>` XML element (as returned by `AirClient.manifest()`) into a `Manifest`.

        Args:
            element: The root `<manifest>` element.

        Returns:
            A populated `Manifest` instance.
        """
        attrs = element.attrib

        messages_el = element.find("messages")
        messages = [m.text for m in messages_el] if messages_el is not None else []

        urls = [ManifestUrl(address=url_el.get("address")) for url_el in element.findall("urls/url")]

        modes = [
            Mode(
                title=mode_el.get("title"),
                protocol=mode_el.get("protocol"),
                port=_int(mode_el.get("port")),
                entry_index=_int(mode_el.get("entry_index")),
                specs=mode_el.get("specs"),
                type=mode_el.get("type"),
                openvpn_minversion=mode_el.get("openvpn_minversion"),
                openvpn_directives=mode_el.get("openvpn_directives"),
                ssh_destination=_int(mode_el.get("ssh_destination")),
            )
            for mode_el in element.findall("modes/mode")
        ]

        rsa = None
        rsa_el = element.find("rsa/RSAParameters")
        if rsa_el is not None:
            exponent_el = rsa_el.find("Exponent")
            modulus_el = rsa_el.find("Modulus")
            rsa = RSAParameters(
                exponent=exponent_el.text if exponent_el is not None else None,
                modulus=modulus_el.text if modulus_el is not None else None,
            )

        servers = [
            ManifestServer(
                name=server_el.get("name"),
                country_code=server_el.get("country_code"),
                location=server_el.get("location"),
                bw_max=_int(server_el.get("bw_max")),
                bw=_int(server_el.get("bw")),
                users=_int(server_el.get("users")),
                users_max=_int(server_el.get("users_max")),
                ips_entry=_csv(server_el.get("ips_entry")),
                ips_exit=_csv(server_el.get("ips_exit")),
                scorebase=_int(server_el.get("scorebase")),
                set=_int(server_el.get("set")),
                group=_int(server_el.get("group")),
                openvpn_directives=server_el.get("openvpn_directives"),
                warning_open=server_el.get("warning_open"),
                warning_closed=server_el.get("warning_closed"),
            )
            for server_el in element.findall("servers/server")
        ]

        servers_groups = [
            ServersGroup(
                support_ipv4=group_el.get("support_ipv4") == "true",
                support_ipv6=group_el.get("support_ipv6") == "true",
                support_check=group_el.get("support_check") == "true",
                ciphers_tls=group_el.get("ciphers_tls"),
                ciphers_tlssuites=group_el.get("ciphers_tlssuites"),
                ciphers_data=group_el.get("ciphers_data"),
                group=_int(group_el.get("group")),
            )
            for group_el in element.findall("servers_groups/servers_group")
        ]

        return cls(
            time=_int(attrs.get("time")),
            next=_int(attrs.get("next")),
            next_update=_int(attrs.get("next_update")),
            dnscheck_host=attrs.get("dnscheck_host"),
            dnscheck_res1=attrs.get("dnscheck_res1"),
            dnscheck_res2=attrs.get("dnscheck_res2"),
            speed_factor=_int(attrs.get("speed_factor")),
            latency_factor=_int(attrs.get("latency_factor")),
            penality_factor=_int(attrs.get("penality_factor")),
            users_factor=_int(attrs.get("users_factor")),
            load_factor=_int(attrs.get("load_factor")),
            ping_factor=_int(attrs.get("ping_factor")),
            pinger_delay=_int(attrs.get("pinger_delay")),
            pinger_retry=_int(attrs.get("pinger_retry")),
            check_domain=attrs.get("check_domain"),
            check_dns_query=attrs.get("check_dns_query"),
            check_protocol=attrs.get("check_protocol"),
            force_reauth_ts=_int(attrs.get("force_reauth_ts")),
            openvpn_directives=attrs.get("openvpn_directives"),
            mode_protocol=attrs.get("mode_protocol"),
            mode_port=_int(attrs.get("mode_port")),
            mode_alt=_int(attrs.get("mode_alt")),
            messages=messages,
            urls=urls,
            modes=modes,
            rsa=rsa,
            servers=servers,
            servers_groups=servers_groups,
        )

    @staticmethod
    def from_string(xml: str) -> Manifest:
        """Parses an XML string into a `Manifest`.

        Args:
            xml: The decrypted XML response string, as returned by `AirClient.request()`.

        Returns:
            A populated `Manifest` instance.
        """
        return Manifest.from_element(ElementTree.fromstring(xml))

    def __str__(self):
        """Returns a short summary of the server count and generation time."""
        return f"Manifest({len(self.servers)} servers, generated at {self.time})"
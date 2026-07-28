import os

from typing import TypedDict, Unpack
from base64 import b64encode
from enum import StrEnum

class VpnType(StrEnum):
    """VPN protocol family supported by the config generator."""
    OPENVPN = "openvpn"
    WIREGUARD = "wireguard"

class ProtocolType(StrEnum):
    """Transport protocol used for the VPN connection."""
    UDP = "udp"
    TCP = "tcp"
    SSH = "ssh"
    SSL = "ssl"

class SystemType(StrEnum):
    """Target operating system for a generated config bundle."""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macosx"
    ANDROID = "android"
    IOS = "ios"
    RPI = "rpi"
    CHROMEOS = "chromeos"
    ROUTER = "other"

class OptionsDict(TypedDict, total=False):
    protocols: str
    servers: str
    download: str
    system: SystemType
    openvpn_version: str
    device: str
    files_binary: str
    files_prefix: str
    openvpn_noembedkeys: bool
    openvpn_directives: str
    openvpn_data_ciphers: str
    resolve: bool
    openvpn_allservers: bool
    proxy_mode: str
    proxy_host: str
    proxy_port: str
    proxy_auth: str
    proxy_login: str
    proxy_password: str
    wireguard_mtu: int
    wireguard_persistent_keepalive: int
    iplayer_entry: str
    iplayer_exit: str

class Options:
    """Mutable container for the parameters used to request a VPN config.

    Instances are typically constructed from the generator API's own
    `options` response payload (via `Options(**option_data)`) and are
    reused/mutated to request individual files from a `ConfigList`
    (e.g. by setting `download` before each request).

    Attributes:
        protocols: List of protocol strings (split from a comma-separated
            string if a string was passed in).
        servers: List of server names (split from a comma-separated string
            if a string was passed in).
        download: Download/file-index selector used for per-file requests.
        system: Target operating system.
        openvpn_version: OpenVPN version string, if applicable.
        device: Device profile name associated with these configs.
        files_binary: Optional bundled binary/executable identifier.
        files_prefix: Optional filename prefix for generated files.
        openvpn_noembedkeys: Whether to omit embedding keys directly in
            OpenVPN configs.
        openvpn_directives: Additional custom OpenVPN directives.
        openvpn_data_ciphers: Custom OpenVPN data cipher list.
        resolve: Whether to resolve hostnames instead of using raw IPs.
        openvpn_allservers: Whether to include all servers in a single
            OpenVPN config.
        proxy_mode: Proxy mode ("none" or a specific proxy type).
        proxy_host: Proxy host address.
        proxy_port: Proxy port.
        proxy_auth: Proxy authentication method/type.
        proxy_login: Proxy authentication username.
        proxy_password: Proxy authentication password.
        wireguard_mtu: MTU value for WireGuard configs.
        wireguard_persistent_keepalive: Persistent keepalive interval, in
            seconds, for WireGuard configs.
        iplayer_entry: IP layer to use for the entry connection.
        iplayer_exit: IP layer to use for the exit connection.
    """
    def __init__(self, **kwargs: Unpack[OptionsDict]):
        protocols = kwargs.get("protocols", [])
        self.protocols = protocols.split(",") if isinstance(protocols, str) else protocols
        servers = kwargs.get("servers", [])
        self.servers = servers.split(",") if isinstance(servers, str) else servers
        self.download = kwargs.get("download")
        self.system = kwargs.get("system")
        self.openvpn_version = kwargs.get("openvpn_version")
        self.device = kwargs.get("device")
        self.files_binary = kwargs.get("files_binary")
        self.files_prefix = kwargs.get("files_prefix")
        self.openvpn_noembedkeys = kwargs.get("openvpn_noembedkeys")
        self.openvpn_directives = kwargs.get("openvpn_directives")
        self.openvpn_data_ciphers = kwargs.get("openvpn_data_ciphers")
        self.resolve = kwargs.get("resolve")
        self.openvpn_allservers = kwargs.get("openvpn_allservers")
        self.proxy_mode = kwargs.get("proxy_mode")
        self.proxy_host = kwargs.get("proxy_host")
        self.proxy_port = kwargs.get("proxy_port")
        self.proxy_auth = kwargs.get("proxy_auth")
        self.proxy_login = kwargs.get("proxy_login")
        self.proxy_password = kwargs.get("proxy_password")
        self.wireguard_mtu = kwargs.get("wireguard_mtu")
        self.wireguard_persistent_keepalive = kwargs.get("wireguard_persistent_keepalive")
        self.iplayer_entry = kwargs.get("iplayer_entry")
        self.iplayer_exit = kwargs.get("iplayer_exit")

    def __str__(self):
        """Return the string form of this instance's `__dict__`."""
        return str(self.__dict__)

    def __hash__(self):
        """Hash based on the integer value of this instance's `__str__()` bytes.

        Note this is derived from `__str__`, so two `Options` instances
        with equal attributes will hash equally.
        """
        return int.from_bytes(str(self).encode())
    
    def clone(self) -> Options:
        """Return a new `Options` instance with a shallow copy of this instance's attributes.

        Since `protocols`/`servers` etc. are passed straight through
        `__init__`, list-valued attributes are re-referenced rather than
        deep-copied unless `__init__` creates a new list (as it does when
        given a comma-separated string). Mutating a cloned list in place
        (e.g. `.append()`) may still affect the original; prefer
        reassignment (e.g. slicing) when working with a clone.

        Returns:
            A new, independent `Options` instance with the same attribute values.
        """
        return Options(**self.__dict__)
    

class Config:
    """A single generated VPN configuration file.

    Attributes:
        filename: The filename this config was stored under in the
            generator's response (e.g. within its zip archive).
        buffer: The raw file contents as bytes.
    """
    def __init__(self, filename: str, buffer: bytes):
        self.filename = filename
        self.buffer = buffer
    
    def write(self, output_dir: str = None):
        """Write this config's contents to disk.

        Args:
            output_dir: Directory to write the file into. Created
                (including parents) if it doesn't already exist. If
                omitted, the file is written to the current working
                directory using `filename` as-is.
        """
        fp = self.filename

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            fp = os.path.join(output_dir, fp)

        with open(fp, "wb") as f:
            f.write(self.buffer)
    
    def read(self) -> str:
        """Return this config's contents as text, decoding if necessary.

        Attempts to decode `buffer` as UTF-8 text, normalizing Windows-style
        line endings ("\\r\\n") to "\\n". If the buffer isn't valid UTF-8
        (e.g. a bundled binary), it's returned as a base64-encoded string
        instead.

        Returns:
            The decoded text with normalized line endings, or a base64-encoded string if the contents aren't valid UTF-8 text.
        """
        try:
            return self.buffer.decode().replace("\r\n", "\n")
        except UnicodeDecodeError:
            return b64encode(self.buffer).decode()
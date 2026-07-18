from typing import TypedDict, Unpack
from enum import StrEnum

class VpnType(StrEnum):
    OPENVPN = "openvpn"
    WIREGUARD = "wireguard"

class ProtocolType(StrEnum):
    UDP = "udp"
    TCP = "tcp"
    SSH = "ssh"
    SSL = "ssl"

class SystemType(StrEnum):
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
    def __init__(self, **kwargs: Unpack[OptionsDict]):
        self.protocols = kwargs.get("protocols", "").split(",")
        self.servers = kwargs.get("servers", "").split(",")
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
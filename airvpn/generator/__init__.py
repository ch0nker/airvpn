# https://airvpn.org/api/generator/?protocols=wireguard_3_udp_1637&servers=xamidimura&device=Default
# https://airvpn.org/api/generator/?protocols=openvpn_3_udp_443%2Copenvpn_3_tcp_443%2Cwireguard_3_udp_1637%2Copenvpn_4_udp_443&servers=asellus&device=Default
# https://airvpn.org/api/generator/?protocols=openvpn_3_udp_443%2Copenvpn_3_tcp_443%2Cwireguard_3_udp_1637%2Copenvpn_4_udp_443&servers=grus%2Casellus&device=Default
# https://airvpn.org/api/generator/?protocols=openvpn_3_udp_443%2Copenvpn_3_tcp_443%2Cwireguard_3_udp_1637%2Copenvpn_4_udp_443&servers=america%2Casia%2Cearth%2Cbr%2Cca%2Cgrus%2Casellus%2Cvulpecula%2Cxamidimura&system=linux&device=Default

from typing import Unpack
from airvpn.network import AirSession
from airvpn.generator.models import SystemType, ProtocolType, VpnType, OptionsDict

class Generator:
    """Generates VPN configuration files via the AirVPN config generator API.

    Wraps the same endpoint used by https://airvpn.org/generator, allowing
    programmatic creation of OpenVPN/WireGuard configs for one or more
    servers, systems, and protocols.

    Access type:
        User-specific, API KEY required.
    """

    KEY_NEEDED = True

    def __init__(self, session: AirSession):
        self.session = session

    def create_config(self,
                  server: str,
                  device: str,
                  system: SystemType = SystemType.WINDOWS,
                  vpn_type: VpnType = VpnType.WIREGUARD,
                  protocol_type: ProtocolType = ProtocolType.UDP,
                  port: int = 1637,
                  entry_ip: int = 3,
                  download: str = "auto",
                  files_binary: str = "",
                  files_prefix: str = "",
                  openvpn_directives: str = "",
                  openvpn_data_ciphers: str = "",
                  resolve: bool = False,
                  openvpn_allserver: bool = False,
                  proxy_mode: str = "none",
                  proxy_host: str = "127.0.0.1",
                  proxy_port: str = "8080",
                  proxy_login: str = "",
                  proxy_password: str = "",
                  proxy_auth: str = "none",
                  wireguard_mtu: int = 1320,
                  wireguard_persistent_keepalive: int = 15,
                  iplayer_entry: str = "ipv4",
                  iplayer_exit: str = "both",
                  **kwargs: Unpack[OptionsDict]
                ):
        """Generate a VPN configuration file for one or more servers.

        Args:
            server: Server name(s) to generate the config for. Multiple
                servers, countries, continents, or "earth" can be combined
                with commas (e.g. "america,asia,earth,br,ca").
            device: The device profile name to associate with this config.
            system: Target operating system for the generated config.
            vpn_type: VPN protocol family (e.g. WireGuard, OpenVPN).
            protocol_type: Transport protocol (UDP or TCP).
            port: Port number to connect on.
            entry_ip: IP version/entry point selector for the connection.
            download: Download mode for the generated files ("auto" or
                a specific format).
            files_binary: Optional binary/executable to bundle with the config.
            files_prefix: Optional filename prefix for generated files.
            openvpn_directives: Additional custom directives to inject into
                an OpenVPN config.
            openvpn_data_ciphers: Custom data cipher list for OpenVPN.
            resolve: Whether to resolve server hostnames instead of using
                raw IPs in the config.
            openvpn_allserver: Whether to include all servers in a single
                OpenVPN config.
            proxy_mode: Proxy mode to configure in the generated config
                ("none" or a specific proxy type).
            proxy_auth: Proxy authentication method/type, if proxy_mode
                    is enabled.
            proxy_host: Proxy host address, if proxy_mode is enabled.
            proxy_port: Proxy port, if proxy_mode is enabled.
            proxy_login: Proxy authentication username, if required.
            proxy_password: Proxy authentication password, if required.
            wireguard_mtu: MTU value for WireGuard configs.
            wireguard_persistent_keepalive: Persistent keepalive interval,
                in seconds, for WireGuard configs.
            iplayer_entry: IP layer to use for the entry connection
                ("ipv4", "ipv6", or "both").
            iplayer_exit: IP layer to use for the exit connection
                ("ipv4", "ipv6", or "both").
            **kwargs: Additional generator options not covered by the named
                parameters above. These override any matching keys built
                from the named parameters. Supported keys include:

                openvpn_version: OpenVPN version to target.
                openvpn_noembedkeys: Whether to omit embedding keys directly
                    in the OpenVPN config (reference external key files instead).
                openvpn_allservers: Whether to include all servers in a single
                    OpenVPN config. Note: this is a separate key from the
                    openvpn_allserver named parameter above and does not
                    override it.

                See OptionsDict for the full list of supported keys.

        Returns:
            The raw text response from the generator endpoint (typically
            the generated config file contents).
        """
        options = locals()

        options.pop("self")
        options.pop("server")
        options.pop("kwargs")

        protocol = f"{vpn_type}_{entry_ip}_{protocol_type}_{port}"

        options["protocols"] = protocol
        options["servers"] = server

        options = options | kwargs

        response = self.session.get("generator", params=options)

        return response.text
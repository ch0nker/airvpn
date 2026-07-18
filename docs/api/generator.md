# Generator

Generates VPN configuration files via the AirVPN config generator API. Wraps the same endpoint used by the [web generator](https://airvpn.org/generator), allowing programmatic creation of OpenVPN/WireGuard configs for one or more servers, systems, and protocols.

**Access type:** User-specific, API key required.

## Methods

### `create_config(server, device, **options) -> str`

Generates a VPN configuration file for one or more servers.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `server` | `str` | — | Server name(s) to generate the config for. Multiple servers, countries, continents, or "earth" can be combined with commas. |
| `device` | `str` | — | The device profile name to associate with this config. |
| `system` | `SystemType` | `WINDOWS` | Target operating system. |
| `vpn_type` | `VpnType` | `WIREGUARD` | VPN protocol family. |
| `protocol_type` | `ProtocolType` | `UDP` | Transport protocol. |
| `port` | `int` | `1637` | Port number to connect on. |
| `entry_ip` | `int` | `3` | IP version/entry point selector. |
| `download` | `str` | `"auto"` | Download mode for generated files. |
| `files_binary` | `str` | `""` | Optional binary/executable to bundle with the config. |
| `files_prefix` | `str` | `""` | Optional filename prefix for generated files. |
| `openvpn_directives` | `str` | `""` | Additional custom directives for OpenVPN. |
| `openvpn_data_ciphers` | `str` | `""` | Custom data cipher list for OpenVPN. |
| `resolve` | `bool` | `False` | Resolve server hostnames instead of using raw IPs. |
| `openvpn_allservers` | `bool` | `False` | Include all servers in a single OpenVPN config. |
| `proxy_mode` | `str` | `"none"` | Proxy mode for the generated config. |
| `proxy_host` | `str` | `"127.0.0.1"` | Proxy host, if `proxy_mode` is enabled. |
| `proxy_port` | `str` | `"8080"` | Proxy port, if `proxy_mode` is enabled. |
| `proxy_login` / `proxy_password` | `str` | `""` | Proxy credentials, if required. |
| `wireguard_mtu` | `int` | `1320` | MTU value for WireGuard configs. |
| `wireguard_persistent_keepalive` | `int` | `15` | Persistent keepalive interval, in seconds. |
| `iplayer_entry` | `str` | `"ipv4"` | IP layer for the entry connection. |
| `iplayer_exit` | `str` | `"both"` | IP layer for the exit connection. |
| `**kwargs` | `OptionsDict` | — | Additional options not listed above (see below). Overrides matching named parameters. |

**Returns:** The raw text response from the generator endpoint (the generated config file contents).

```py
config = api.generator.create_config(
    server="earth",
    device="Default",
    vpn_type=VpnType.WIREGUARD,
    protocol_type=ProtocolType.UDP,
    port=1637,
)
```

## Additional `**kwargs` options

| Key | Type | Description |
|---|---|---|
| `openvpn_version` | `str` | OpenVPN version to target. |
| `openvpn_noembedkeys` | `bool` | Omit embedding keys directly in the OpenVPN config. |
| `proxy_auth` | `str` | Proxy authentication method/type. |

# Generator

Generates VPN configuration files via the AirVPN config generator API. Wraps the same endpoint used by the [web generator](https://airvpn.org/generator), allowing programmatic creation of OpenVPN/WireGuard configs for one or more servers, systems, and protocols.

**Access type:** User-specific, API key required.

## Methods

### `create(servers, device, **options) -> ConfigList | str`

Requests the configuration generator with `download="auto"` and returns the generated configuration file(s). When the generator returns a single file directly, its contents are returned as a `str`. When the generator instead reports a set of files (some configuration options produce multiple files, even for a single server), a `ConfigList` is returned — a lazily-fetched, sliceable, iterable collection covering those files. Individual files aren't downloaded until you access them (by index, slice, or iteration), and each fetched file is cached afterward.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `servers` | `str \| list[str]` | — | Server name(s) to generate configs for. Accepts a single server/country/continent name (e.g. `"earth"`) or a list of them, which will be comma-joined. Multiple servers, or planets can be combined with commas (e.g. `"earth, "`). |
| `device` | `str` | — | The device profile name to associate with these configs. |
| `system` | `SystemType` | `WINDOWS` | Target operating system. |
| `vpn_type` | `VpnType` | `WIREGUARD` | VPN protocol family. |
| `protocol_type` | `ProtocolType` | `UDP` | Transport protocol. |
| `port` | `int` | `1637` | Port number to connect on. |
| `entry_ip` | `int` | `3` | IP version/entry point selector. |
| `files_binary` | `str` | `""` | Optional binary/executable to bundle with the configs. |
| `files_prefix` | `str` | `""` | Optional filename prefix for generated files. |
| `openvpn_directives` | `str` | `""` | Additional custom directives for OpenVPN. |
| `openvpn_data_ciphers` | `str` | `""` | Custom data cipher list for OpenVPN. |
| `resolve` | `bool` | `False` | Resolve server hostnames instead of using raw IPs. |
| `openvpn_allservers` | `bool` | `False` | Include all servers in a single OpenVPN config. |
| `proxy_mode` | `str` | `"none"` | Proxy mode for the generated config. |
| `proxy_host` | `str` | `"127.0.0.1"` | Proxy host, if `proxy_mode` is enabled. |
| `proxy_port` | `str` | `"8080"` | Proxy port, if `proxy_mode` is enabled. |
| `proxy_login` / `proxy_password` | `str` | `""` | Proxy credentials, if required. |
| `proxy_auth` | `str` | `"none"` | Proxy authentication method/type, if `proxy_mode` is enabled. |
| `wireguard_mtu` | `int` | `1320` | MTU value for WireGuard configs. |
| `wireguard_persistent_keepalive` | `int` | `15` | Persistent keepalive interval, in seconds. |
| `iplayer_entry` | `str` | `"ipv4"` | IP layer for the entry connection. |
| `iplayer_exit` | `str` | `"both"` | IP layer for the exit connection. |
| `**kwargs` | `OptionsDict` | — | Additional options not listed above (see below). Used primarily for per-server download selection, e.g. `server_earth="on"`. |

**Returns:** A `str` with the config file's contents (Windows-style line endings normalized to `"\n"`) when exactly one file is generated; otherwise a `ConfigList` covering all generated files. See [`ConfigList`](#configlist) below.

```py
config = api.generator.create(
    servers="earth",
    device="Default",
    vpn_type=VpnType.WIREGUARD,
    protocol_type=ProtocolType.UDP,
    port=1637,
)
```

### `download(output_dir, servers, device, **options) -> None`

Generates VPN configuration file(s) for one or more servers and writes them to disk. Always requests a zip bundle from the generator endpoint (`download` is forced to `"zip"` internally) and extracts its contents directly into `output_dir`, creating the directory if it doesn't already exist.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `output_dir` | `str` | — | Directory to extract the generated config files into. Created (including parents) if it doesn't already exist. |
| `servers` | `str \| list[str]` | — | Server name(s) to generate configs for. Accepts a single server/country/continent name (e.g. `"earth"`) or a list of them, which will be comma-joined. Multiple servers, countries, continents, or "earth" can be combined with commas (e.g. `"america,asia,earth,br,ca"`). Note this always requests a zip bundle and extracts everything the API returns, which may include more than one file even for a single server (e.g. SSH configs). |
| `device` | `str` | — | The device profile name to associate with these configs. |
| `system` | `SystemType` | `WINDOWS` | Target operating system. |
| `vpn_type` | `VpnType` | `WIREGUARD` | VPN protocol family. |
| `protocol_type` | `ProtocolType` | `UDP` | Transport protocol. |
| `port` | `int` | `1637` | Port number to connect on. |
| `entry_ip` | `int` | `3` | IP version/entry point selector. |
| `files_binary` | `str` | `""` | Optional binary/executable to bundle with the configs. |
| `files_prefix` | `str` | `""` | Optional filename prefix for generated files. |
| `openvpn_directives` | `str` | `""` | Additional custom directives for OpenVPN. |
| `openvpn_data_ciphers` | `str` | `""` | Custom data cipher list for OpenVPN. |
| `resolve` | `bool` | `False` | Resolve server hostnames instead of using raw IPs. |
| `openvpn_allservers` | `bool` | `False` | Include all servers in a single OpenVPN config. |
| `proxy_mode` | `str` | `"none"` | Proxy mode for the generated config. |
| `proxy_host` | `str` | `"127.0.0.1"` | Proxy host, if `proxy_mode` is enabled. |
| `proxy_port` | `str` | `"8080"` | Proxy port, if `proxy_mode` is enabled. |
| `proxy_login` / `proxy_password` | `str` | `""` | Proxy credentials, if required. |
| `proxy_auth` | `str` | `"none"` | Proxy authentication method/type, if `proxy_mode` is enabled. |
| `wireguard_mtu` | `int` | `1320` | MTU value for WireGuard configs. |
| `wireguard_persistent_keepalive` | `int` | `15` | Persistent keepalive interval, in seconds. |
| `iplayer_entry` | `str` | `"ipv4"` | IP layer for the entry connection. |
| `iplayer_exit` | `str` | `"both"` | IP layer for the exit connection. |
| `**kwargs` | `OptionsDict` | — | Additional options not listed above (see below). Used primarily for per-server download selection, e.g. `server_earth="on"`. |

```py
api.generator.download(
    output_dir="./configs",
    servers="earth",
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

## `ConfigList`

Returned by [`create`](#createservers-device-options---configlist--str) whenever more than one file is generated. A `ConfigList` behaves like a read-only sequence of `Config` objects, but fetches each file lazily — nothing is downloaded until you actually access it, and each downloaded file is cached for reuse.

```py
configs = api.generator.create(
    servers="earth",
    device="Default",
)

len(configs)          # number of files available
configs[0]             # fetches (or returns the cached) first Config
configs[-1]            # supports negative indexing
configs[1:3]           # returns a new, independent ConfigList for just that slice

for config in configs:  # iterates, fetching each file in turn
    config.write("./configs")
```

**Indexing (`configs[i]`)** — Fetches and returns the `Config` at index `i` (0-based; negative indices count from the end). The result is cached, so accessing the same index again doesn't re-fetch it.

**Slicing (`configs[start:stop:step]`)** — Returns a new `ConfigList` scoped to just the sliced files. This is independent of the original: it doesn't share fetch state beyond what was already cached, and generating configs from it won't affect the original list.

**Iteration (`for config in configs`)** — Yields each `Config` in order, fetching as it goes. Multiple simultaneous loops over the same `ConfigList` don't interfere with each other.

**Equality/hashing** — Two `ConfigList` instances are equal (and hash equally) if their generation `Options` are equal — i.e. they'd produce the same files.

### `Config`

A single generated configuration file, as returned by indexing/iterating a `ConfigList`.

| Attribute/Method | Description |
|---|---|
| `filename` | The filename this config was stored under (e.g. within the generator's zip archive). |
| `buffer` | The raw file contents, as `bytes`. |
| `read() -> str` | Returns the contents as text (Windows-style line endings normalized to `"\n"`). If the contents aren't valid UTF-8 (e.g. a bundled binary from `files_binary`), returns a base64-encoded string instead. |
| `write(output_dir=None) -> None` | Writes the file to disk under `filename`. If `output_dir` is given, it's created (including parents) if needed and the file is written inside it; otherwise the file is written to the current working directory. |
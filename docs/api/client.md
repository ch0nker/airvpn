# AirClient

Low-level client for AirVPN's legacy bootstrap-based protocol, used to authenticate and exchange encrypted requests with AirVPN's `bluetit` service directly — independent of the `AirSession`/service classes documented elsewhere in these docs.

It fetches a runtime configuration (`.rc`) file to discover the current bootstrap servers and RSA key material, then wraps each request's parameters in a hybrid RSA+AES encryption scheme before POSTing to one of those servers and decrypting the response.

```py
from airvpn.airclient import AirClient

client = AirClient()
user = client.login("myusername", "mypassword")
```

> **Note:** This is a separate, lower-level protocol from the REST API used by [`AirVPN`](airvpn.md) and its services. Use `AirClient` only if you specifically need bootstrap-based authentication (e.g. mirroring what the official clients do) rather than the api-key–based REST API.

## Class Attributes

| Attribute | Type | Description |
|---|---|---|
| `RC_URL` | `str` | URL of the AirVPN runtime configuration file used to discover bootstrap servers and RSA key parameters. |

## Constructor

```py
AirClient()
```

Takes no arguments. Creates a `requests.Session()` internally for making HTTP requests.

## Methods

### `parse_rc() -> dict[str, str | list[str]]`

Fetches and parses the `.rc` configuration file at `RC_URL` into a dictionary. Lines are matched as `key value` pairs; if the same key appears more than once, its values are collected into a list.

**Returns:** A dict mapping config keys (e.g. `bootserver`, `rsamodulus`, `rsaexponent`) to either a single string or a list of strings, depending on how many times the key appeared.

---

### `system_description() -> str`

Returns the current system's platform name (`platform.system()`), e.g. `"Linux"`, `"Windows"`, `"Darwin"`.

---

### `architecture() -> str`

Returns the current system's machine architecture (`platform.machine()`), e.g. `"x86_64"`.

---

### `b64_map(params: dict) -> str`

Encodes a dict of parameters into AirVPN's newline-delimited, base64-encoded `key:value` wire format, used as the plaintext input to encryption.

| Parameter | Type | Description |
|---|---|---|
| `params` | `dict` | Parameters to encode. Values may be `bytes` or any type coercible to `str`. |

**Returns:** A string with one `base64(key):base64(value)` pair per line.

---

### `decrypt_response(response_content: bytes, secret_key: bytes, iv: bytes) -> str`

Decrypts an AES-CBC–encrypted API response using the session's secret key and IV, and removes PKCS#7 padding.

| Parameter | Type | Description |
|---|---|---|
| `response_content` | `bytes` | The raw encrypted response body. |
| `secret_key` | `bytes` | The AES key used for this request/response pair. |
| `iv` | `bytes` | The AES initialization vector used for this request/response pair. |

**Returns:** The decrypted plaintext as a `str`.

**Raises:**
- `AESDecryptionError` — if unpadding fails (e.g. the key/IV don't match, or the content is corrupted).

---

### `build_encrypted_params(rsa_modulus_b64, rsa_exponent_b64, params, key_size=32, iv_size=16) -> tuple[bytes, bytes, bytes, bytes]`

Generates a random AES key and IV, RSA-encrypts them (PKCS#1 v1.5) alongside the AES key/IV pair itself, and AES-encrypts the given request parameters with that key. This is the encryption step used internally by [`request()`](#requestaction-str-kwargs).

| Parameter | Type | Description |
|---|---|---|
| `rsa_modulus_b64` | `str` | Base64-encoded RSA public key modulus (from `parse_rc()`'s `rsamodulus`). |
| `rsa_exponent_b64` | `str` | Base64-encoded RSA public key exponent (from `parse_rc()`'s `rsaexponent`). |
| `params` | `dict` | The request parameters to AES-encrypt. |
| `key_size` | `int` | Size in bytes of the generated AES key. Defaults to `32`. |
| `iv_size` | `int` | Size in bytes of the generated AES IV. Defaults to `16`. |

**Returns:** A 4-tuple `(assoc_params, data_params, secret_key, iv)`:
- `assoc_params` (`bytes`) — the RSA-encrypted key/IV association blob (sent as `s`).
- `data_params` (`bytes`) — the AES-encrypted request parameters (sent as `d`).
- `secret_key` (`bytes`) — the generated AES key, needed to decrypt the response.
- `iv` (`bytes`) — the generated AES IV, needed to decrypt the response.

**Raises:**
- `RSAError` — if RSA encryption of the key/IV association blob fails.
- `AESEncryptionError` — if AES encryption of the request parameters fails.

---

### `request(action: str, **kwargs) -> str | None`

Performs a full round-trip request to the AirVPN bootstrap API: fetches and parses the `.rc` file, encrypts the given action and parameters, POSTs to each bootstrap server (tried one at a time, in random order) until one responds, and decrypts the response. A server that can't be connected to is skipped in favor of the next one; a server that responds with a non-`200` status or an empty body is also skipped. Used internally by [`login()`](#loginusername-str-password-str) and [`manifest()`](#manifest).

| Parameter | Type | Description |
|---|---|---|
| `action` | `str` | The API action to perform (e.g. `"user"`, `"manifest"`). |
| `**kwargs` | | Additional parameters for the action. `system`, `version`, `software`, and `arch` are auto-filled with sensible defaults if not provided. |

**Returns:** The decrypted response body as a raw XML `str`. Returns `None` if every bootstrap server fails to connect or respond with a `200` and non-empty body.

**Raises:**
- `RCParseError` — if `rsamodulus`/`rsaexponent` can't be found in the parsed `.rc` file.
- `RSAError` / `AESEncryptionError` — if building the encrypted request parameters fails.
- `AESDecryptionError` — if decrypting a server's response fails.

---

### `login(username: str, password: str) -> User | None`

Authenticates with the given credentials and parses the response into a [`User`](#user).

```py
user = client.login("myusername", "mypassword")
```

| Parameter | Type | Description |
|---|---|---|
| `username` | `str` | AirVPN account username. |
| `password` | `str` | AirVPN account password. |

**Returns:** A [`User`](#user) built from the parsed XML response, containing the account's connection credentials. Returns `None` if no bootstrap server could be reached (see [`request()`](#requestaction-str-kwargs)).

**Raises:**
- `LoginError` — if the response's `message_action` is `"stop"` (login rejected; `LoginError`'s message is the server's `message`).
- Same as [`request()`](#requestaction-str-kwargs) for any lower-level request/encryption failures.

---

### `manifest() -> Manifest | None`

Retrieves the AirVPN manifest (server list, connection modes, and bootstrap metadata) and parses it into a [`Manifest`](#manifest-1).

```py
manifest = client.manifest()
```

**Returns:** A [`Manifest`](#manifest-1) built from the parsed XML response. Returns `None` if no bootstrap server could be reached (see [`request()`](#requestaction-str-kwargs)).

**Raises:** Same as [`request()`](#requestaction-str-kwargs).

---

## Response Models

`login()` and `manifest()` don't return raw XML — they return typed objects parsed from it, defined alongside `AirClient`. Each model also exposes a `from_element(element: ElementTree.Element)` classmethod and, where used as a request's top-level response, a `from_string(xml: str)` classmethod for parsing directly from an `ElementTree.Element` / XML string.

### `User`

The parsed response from `login()` — the authenticated account's connection credentials.

| Attribute | Type | Description |
|---|---|---|
| `ts` | `int` | Unix timestamp the response was generated. |
| `login` | `str` | The account's username. |
| `expiration_date` | `str` | The account's expiration date. |
| `ca` | `str` | The OpenVPN CA certificate. |
| `ta` | `str` | The OpenVPN TLS-auth key. |
| `tls_crypt` | `str` | The OpenVPN tls-crypt key. |
| `ssh_key` | `str` | The SSH tunnel private key. |
| `ssh_ppk` | `str` | The SSH tunnel private key in PPK format. |
| `ssl_crt` | `str` | The SSL/stunnel certificate. |
| `wg_public_key` | `str` | The server's WireGuard public key. |
| `keys` | `list[Key]` | Devices/keys registered to this account. |
| `message` | `str` | A message from the server, if any (e.g. describing a login failure). |
| `message_action` | `str` | The action associated with `message`, e.g. `"stop"` when login fails. |

### `Key`

A device's certificates/keys issued to a user's account, found in `User.keys`.

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | The device/key's name. |
| `crt` | `str` | The device's OpenVPN certificate. |
| `key` | `str` | The device's OpenVPN private key. |
| `wg_private_key` | `str` | The device's WireGuard private key. |
| `wg_preshared` | `str` | The device's WireGuard preshared key. |
| `wg_ipv4` | `str` | The device's assigned WireGuard IPv4 address. |
| `wg_ipv6` | `str` | The device's assigned WireGuard IPv6 address. |
| `wg_dns_ipv4` | `str` | The IPv4 DNS server to use for this device's WireGuard connection. |
| `wg_dns_ipv6` | `str` | The IPv6 DNS server to use for this device's WireGuard connection. |

### `Manifest`

The parsed response from `manifest()` — the bootstrap manifest, including the server list, connection modes, and client configuration.

| Attribute | Type | Description |
|---|---|---|
| `time` | `int` | Unix timestamp this manifest was generated. |
| `next` | `int` | Unix timestamp the next manifest update is expected. |
| `next_update` | `int` | Number of seconds until the next expected update. |
| `dnscheck_host` | `str` | Hostname used for DNS-based connectivity checks. |
| `dnscheck_res1` | `str` | Expected DNS check response IP, primary. |
| `dnscheck_res2` | `str` | Expected DNS check response IP, secondary. |
| `speed_factor` | `int` | Weight given to speed in server scoring. |
| `latency_factor` | `int` | Weight given to latency in server scoring. |
| `penality_factor` | `int` | Weight given to penalties in server scoring. |
| `users_factor` | `int` | Weight given to user count in server scoring. |
| `load_factor` | `int` | Weight given to load in server scoring. |
| `ping_factor` | `int` | Weight given to ping in server scoring. |
| `pinger_delay` | `int` | Delay in seconds between pinger runs. |
| `pinger_retry` | `int` | Number of pinger retries. |
| `check_domain` | `str` | Domain used for connectivity checks. |
| `check_dns_query` | `str` | DNS query template used for connectivity checks. |
| `check_protocol` | `str` | Protocol used for connectivity checks (e.g. `"https"`). |
| `force_reauth_ts` | `int` | Unix timestamp after which reauthentication is forced. |
| `openvpn_directives` | `str` | Default OpenVPN config directives applied across modes. |
| `mode_protocol` | `str` | Default transport protocol for connections. |
| `mode_port` | `int` | Default port for connections. |
| `mode_alt` | `int` | Alternate mode indicator. |
| `messages` | `list[str]` | Operator messages/announcements included in the manifest. |
| `urls` | `list[ManifestUrl]` | Bootstrap server URLs. |
| `modes` | `list[Mode]` | Connection modes available (protocol/port/type combinations). |
| `rsa` | `RSAParameters \| None` | The RSA public key used to encrypt requests, if present. |
| `servers` | `list[ManifestServer]` | Every VPN server known to the manifest. |
| `servers_groups` | `list[ServersGroup]` | Shared connection capabilities, keyed by server group. |

`str(manifest)` returns a short summary, e.g. `"Manifest(214 servers, generated at 1719000000)"`.

### `ManifestServer`

A single VPN server entry, found in `Manifest.servers`.

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | The server's public name. |
| `country_code` | `str` | ISO country code of the server's location. |
| `location` | `str` | City/region of the server. |
| `bw_max` | `int` | Maximum bandwidth available, in Mbit/s. |
| `bw` | `int` | Bandwidth currently in use, in bytes. |
| `users` | `int` | Number of users currently connected. |
| `users_max` | `int` | Maximum number of users this server accepts. |
| `ips_entry` | `list[str]` | Entry IP addresses (IPv4 and IPv6), indexed by a mode's `entry_index`. |
| `ips_exit` | `list[str]` | Exit IP addresses (IPv4 and IPv6) traffic appears to originate from. |
| `scorebase` | `int` | Base score used in server selection/ranking. |
| `set` | `int \| None` | Server set identifier, if applicable. |
| `group` | `int` | Server group identifier, matches a `ServersGroup.group`. |
| `openvpn_directives` | `str \| None` | Extra server-specific OpenVPN config directives, if any. |
| `warning_open` | `str \| None` | A warning shown for an otherwise-open server (e.g. elevated packet loss), if any. |
| `warning_closed` | `str \| None` | Reason the server is closed/unavailable (e.g. maintenance), if any. |

**Property:** `is_closed -> bool` — whether the server is currently marked unavailable (i.e. `warning_closed is not None`).

`str(server)` returns the server's public name.

### `Mode`

A connection mode offered by a server (a protocol/port/type combination), found in `Manifest.modes`.

| Attribute | Type | Description |
|---|---|---|
| `title` | `str` | Human-readable description of the mode. |
| `protocol` | `str` | Transport protocol (e.g. `"udp"`, `"tcp"`, `"ssh"`, `"ssl"`). |
| `port` | `int` | Port number to connect to. |
| `entry_index` | `int` | Index into a server's `ips_entry` list to use for this mode. |
| `specs` | `str \| None` | Extra TLS/connection specs (e.g. `"tls-crypt, tls1.2"`), if any. |
| `type` | `str` | VPN type for this mode (e.g. `"wireguard"`, `"openvpn"`). |
| `openvpn_minversion` | `str \| None` | Minimum required OpenVPN version, if applicable. |
| `openvpn_directives` | `str \| None` | Extra OpenVPN config directives specific to this mode, if any. |
| `ssh_destination` | `int` | SSH tunnel destination port, or `0` if not applicable. |

### `RSAParameters`

The RSA public key used to encrypt requests to the bootstrap servers, found in `Manifest.rsa`.

| Attribute | Type | Description |
|---|---|---|
| `exponent` | `str` | Base64-encoded RSA public key exponent. |
| `modulus` | `str` | Base64-encoded RSA public key modulus. |

### `ServersGroup`

Shared connection capabilities for a group of servers, found in `Manifest.servers_groups`.

| Attribute | Type | Description |
|---|---|---|
| `support_ipv4` | `bool` | Whether servers in this group support IPv4. |
| `support_ipv6` | `bool` | Whether servers in this group support IPv6. |
| `support_check` | `bool` | Whether servers in this group support connectivity checks. |
| `ciphers_tls` | `str` | Colon-separated list of supported TLS key-exchange ciphers. |
| `ciphers_tlssuites` | `str` | Colon-separated list of supported TLS 1.3 cipher suites. |
| `ciphers_data` | `str` | Colon-separated list of supported data-channel ciphers. |
| `group` | `int` | The server group identifier these settings apply to. |

### `ManifestUrl`

A bootstrap server URL, found in `Manifest.urls`.

| Attribute | Type | Description |
|---|---|---|
| `address` | `str` | The bootstrap server's URL. |

`str(manifest_url)` returns `address`.

## Exceptions

Raised by various methods above, all defined in `airvpn.exceptions`:

| Exception | Raised when |
|---|---|
| `RCParseError` | `rsamodulus`/`rsaexponent` are missing from the parsed `.rc` file. |
| `RSAError` | RSA encryption of the key/IV association blob fails. |
| `AESEncryptionError` | AES encryption of request parameters fails (or wraps an `RSAError`/`AESEncryptionError` raised while building encrypted params inside `request()`). |
| `AESDecryptionError` | AES decryption/unpadding of a server's response fails. |
| `LoginError` | `login()`'s response has `message_action == "stop"`; the exception's message is the server's `message`. |
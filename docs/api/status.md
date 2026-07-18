# Status

Represents the full VPN network status response — every server, routing node, and aggregate rollup by country, continent, and planet.

**Access type:** Public, no API key required.

```py
status = api.status

for server in status.servers:
    print(server.public_name, server.currentload)
```

## Attributes

| Attribute | Type | Description |
|---|---|---|
| `servers` | `list[Server]` | Individual VPN servers and their current status. |
| `routing` | `list[Routing]` | Routing nodes and their current status. |
| `countries` | `list[Country]` | Aggregate VPN status per country. |
| `continents` | `list[Continent]` | Aggregate VPN status per continent. |
| `planets` | `list[Planet]` | Aggregate VPN status globally (typically a single entry). |
| `deprecated_warning` | `str \| None` | A warning about deprecated fields in the response, if present. |
| `result` | `Status` (network status enum) | Whether the overall request succeeded. |

## Model — `Server`

Represents a single VPN server.

| Attribute | Type | Description |
|---|---|---|
| `public_name` | `str` | The server's public display name. |
| `country_name` / `country_code` | `str` | Country where the server is located. |
| `location` | `str` | Specific city/region of the server. |
| `continent` | `str` | Continent where the server is located. |
| `bw` / `bw_max` | `int` | Bandwidth in use / available, in Mbit/s. |
| `users` | `int` | Number of users currently connected. |
| `currentload` | `int` | Current load as a percentage. |
| `ip_v4_in1`–`ip_v4_in4` | `str` | IPv4 addresses for incoming connections. |
| `ip_v6_in1`–`ip_v6_in4` | `str` | IPv6 addresses for incoming connections. |
| `health` | `str` | Server health status (`ok`, `warning`, or `error`). A server in error status does not accept connections. |
| `warning` | `str \| None` | Reason for a non-`ok` health status, if applicable. |

## Model — `Routing`

Represents a routing node's status (no user/IP data attached).

| Attribute | Type | Description |
|---|---|---|
| `public_name` | `str` | The node's public display name. |
| `country_name` / `country_code` | `str` | Country where the node is located. |
| `location` | `str` | Specific city/region of the node. |
| `continent` | `str` | Continent where the node is located. |
| `bw` / `bw_max` | `int` | Bandwidth in use / available, in Mbit/s. |
| `currentload` | `int` | Current load as a percentage. |
| `health` | `str` | Node health status. |
| `warning` | `str \| None` | Reason for a non-`ok` health status, if applicable. |

## Model — `Country`

Represents aggregate VPN status for a country.

| Attribute | Type | Description |
|---|---|---|
| `country_name` / `country_code` | `str` | The country's name/ISO code. |
| `server_best` | `str` | The recommended server for this country. |
| `bw` / `bw_max` | `int` | Bandwidth in use / available across the country, in Mbit/s. |
| `users` | `int` | Number of users currently connected in this country. |
| `servers` | `int` | Number of servers available in this country. |
| `currentload` | `int` | Current load as a percentage. |
| `ip_v4_in1`–`ip_v4_in4` | `str` | IPv4 hostnames for incoming connections. |
| `ip_v6_in1`–`ip_v6_in4` | `str` | IPv6 hostnames for incoming connections. |
| `health` | `str` | Aggregate health status. |
| `warning` | `str \| None` | Reason for a non-`ok` health status, if applicable. |

## Model — `Continent`

Represents aggregate VPN status for a continent. Same shape as `Country`, without `country_name`/`country_code`; uses `public_name` instead.

## Model — `Planet`

Represents aggregate VPN status for the whole planet (global stats). Same shape as `Continent`.
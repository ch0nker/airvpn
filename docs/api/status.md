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
| `servers` | `StatusList[Server]` | Individual VPN servers and their current status. |
| `routing` | `StatusList[Routing]` | Routing nodes and their current status. |
| `countries` | `StatusList[Country]` | Aggregate VPN status per country. |
| `continents` | `StatusList[Continent]` | Aggregate VPN status per continent. |
| `planets` | `StatusList[Planet]` | Aggregate VPN status globally (typically a single entry). |
| `deprecated_warning` | `str \| None` | A warning about deprecated fields in the response, if present. |

## `StatusList`

Returned by most status endpoints (such as servers, countries, and other status collections). A `StatusList` behaves like a read-only sequence of model instances, but constructs each object lazily — raw API data is stored internally and converted into the appropriate model only when you actually access it. Constructed objects are cached, so repeated access to the same item doesn't rebuild it.

```py
servers = api.servers.list()

len(servers)       # number of servers
servers[0]         # returns the first Server
servers[-1]        # supports negative indexing
servers[1:3]       # returns a new StatusList containing the slice

for server in servers:
    print(server.name)
```

**Indexing (`statuses[i]`)** — Returns the model instance at index `i` (0-based; negative indices count from the end). The object is constructed on first access and then cached for future use.

**Slicing (`statuses[start:stop:step]`)** — Returns a new `StatusList` containing only the sliced items. The new list is independent of the original and maintains its own cache.

**Iteration (`for item in statuses`)** — Yields each model instance in order, constructing and caching items as needed. Multiple simultaneous loops over the same `StatusList` don't interfere with each other.

**Lazy construction** — Objects are not created when the `StatusList` is returned from the API. Raw response data is retained internally and converted into model instances only when accessed.

**Caching** — Once an item has been constructed, it is stored internally and reused for all future accesses to that index.

**Equality/hashing** — `StatusList` does not define custom equality or hashing behavior. Two instances compare by object identity, like normal Python objects.

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
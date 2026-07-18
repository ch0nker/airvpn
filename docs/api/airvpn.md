# AirVPN

Main entry point for interacting with the AirVPN API. Provides access to all available services as lazily-created, cached properties, plus convenience methods for one-off actions.

```py
from airvpn import AirVPN

api = AirVPN(API_KEY)
```

## Constructor

```py
AirVPN(API_KEY: str = None)
```

| Parameter | Type | Description |
|---|---|---|
| `API_KEY` | `str \| None` | Your AirVPN API key. Required for user-specific services (devices, DNS lists, generator, user info, notifications, disconnect). Not required for public services (`whatismyip`, `status`). |

## Properties

Each property lazily creates and caches its corresponding service on first access.

| Property | Returns | API Key Required |
|---|---|---|
| `devices` | [`Devices`](devices.md) | Yes |
| `dns_lists` | [`DnsLists`](dns_lists.md) | No |
| `generator` | [`Generator`](generator.md) | Yes |
| `status` | [`Status`](status.md) | No |
| `userinfo` | [`UserInfo`](userinfo.md) | Yes |
| `whatismyip` | [`WhatIsMyIp`](whatismyip.md) | No |

```py
api.status.servers        # list[Server]
api.userinfo.login
api.whatismyip.ip
```

## Methods

### `get_service(service: str)`

Instantiates a named service class, enforcing its API key requirement. Mostly used internally by the properties above, but exposed publicly in case you need it directly.

| Parameter | Type | Description |
|---|---|---|
| `service` | `str` | The service name (e.g. `"devices"`, `"status"`), matched case-insensitively. |

**Raises:**
- `AssertionError` — if the service name is invalid.
- `Exception` — if the service requires an API key and none was provided.

---

### `send_notification(subject: str, body: str) -> bool`

Sends a message to yourself. See [notification](notification.md) for full details.

```py
api.send_notification("Script finished", "The backup job completed successfully.")
```

**Access type:** User-specific, API key required.

---

### `disconnect(server=None, device=None, server_name=None, device_id=None) -> int`

Requests a disconnection. If no filter parameters are given, disconnects all sessions for the user. See [disconnect](disconnect.md) for full details.

```py
api.disconnect()                       # disconnect everything
api.disconnect(server_name="Achernar") # disconnect one server
```

**Access type:** User-specific, API key required.
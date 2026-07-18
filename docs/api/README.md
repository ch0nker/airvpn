# API Documentation

Reference documentation for every service exposed by the `AirVPN` client.

## Services

| Service | Description | API Key Required |
|---|---|---|
| [AirVPN](airvpn.md) | Main entry point, lazily exposes all services below | Depends on service used |
| [Devices](devices.md) | List, add, delete, renew, and modify registered devices | Yes |
| [DnsLists](dns_lists.md) | Fetch available DNS filtering lists | Unclear (see notes) |
| [Generator](generator.md) | Generate OpenVPN/WireGuard configuration files | Yes |
| [Status](status.md) | Network status: servers, routing, countries, continents, planets | No |
| [UserInfo](userinfo.md) | Account and connection details for the authenticated user | Yes |
| [WhatIsMyIp](whatismyip.md) | Detected IP address and geolocation info | No |
| [disconnect](disconnect.md) | Force-disconnect one or more active sessions | Yes |
| [send_notification](notification.md) | Send yourself a notification via the AirVPN website/email | Yes |

## Quick Start

```py
from airvpn import AirVPN

api = AirVPN(API_KEY)

print(api.userinfo.login)
```

See each service's page for full details on available methods, parameters, and return types.
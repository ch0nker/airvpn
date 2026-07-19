# API Documentation

Reference documentation for every service exposed by the `AirVPN` client.

## Services

| Service | Description | API Key Required |
|---|---|---|
| [AirVPN](airvpn.md) | Main entry point, lazily exposes all services below | Depends on service used |
| [Devices](devices.md) | List, add, delete, renew, and modify registered devices | Yes |
| [DnsLists](dns_lists.md) | Fetch available DNS filtering lists | No |
| [Generator](generator.md) | Generate OpenVPN/WireGuard configuration files | Yes |
| [Status](status.md) | Network status: servers, routing, countries, continents, planets | No |
| [UserInfo](userinfo.md) | Account and connection details for the authenticated user | Yes |
| [WhatIsMyIp](whatismyip.md) | Detected IP address and geolocation info | No |
| [disconnect](disconnect.md) | Force-disconnect one or more active sessions | Yes |
| [send_notification](notification.md) | Send yourself a notification via the AirVPN website/email | Yes |

## Quick Start

Without an API key:
```py
from airvpn import AirVPN

api = AirVPN()

for server in api.status.servers:
    print(server.public_name)
```

With an API key:
```py
import os

from airvpn import AirVPN
from dotenv import load_dotenv

load_dotenv()

api = AirVPN(os.getenv("API_KEY"))
device = api.devices.get("test", create=True)

api.generator.write_config("AirVPN-Earth.conf", "earth", device.id)
```

See each service's page for full details on available methods, parameters, and return types.
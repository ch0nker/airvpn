# API Documentation

Reference documentation for the `AirVPN` API.

## Clients
 
| Class | Description |
|---|---|
| [AirVPN](airvpn.md) | Main entry point; lazily exposes the services below as cached properties |
| [AirClient](client.md) | Legacy bootstrap-based (RSA+AES encrypted) protocol client, separate from the REST API used by `AirVPN` — a standalone class you instantiate yourself |

## Services

| Service | Description | API Key Required |
|---|---|---|
| [Devices](devices.md) | List, add, delete, renew, and modify registered devices | Yes |
| [DnsLists](dns_lists.md) | Fetch available DNS filtering lists | No |
| [Generator](generator.md) | Generate OpenVPN/WireGuard configuration files | Yes |
| [Status](status.md) | Network status: servers, routing, countries, continents, planets | No |
| [UserInfo](userinfo.md) | Account and connection details for the authenticated user | Yes |
| [WhatIsMyIp](whatismyip.md) | Detected IP address and geolocation info | No |
| [Disconnect](disconnect.md) | Force-disconnect one or more active sessions | Yes |
| [Notification](notification.md) | Send yourself a notification via the AirVPN website/email | Yes |

## Other
| Name | Description |
| --- | --- |
| [Exceptions](exceptions.md) | Exception hierarchy raised across the wrapper | 

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

api.generator.download("AirVPN-Earth.conf", "earth", device.id)
```

See each service's page for full details on available methods, parameters, and return types.
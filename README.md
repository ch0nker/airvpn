# Python AirVPN Wrapper

> **Note:** The docstrings and most of the documentation was generated with AI. If you spot any errors I haven't caught yet, please open a PR or an issue.

A Python wrapper for AirVPN's [API](https://airvpn.org/apisettings/).

## Guide
- [Changelog](docs/CHANGELOG.md)
- [Contributing](docs/CONTRIBUTING.md)
- [Example](#example)
- [API Documentation](docs/api/README.md)
- [Test Documentation](docs/tests/README.md)

## Installation
```bash
pip install airvpn
```

## Example
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
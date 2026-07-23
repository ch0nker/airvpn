# Python AirVPN Wrapper

[![Python versions](https://img.shields.io/pypi/pyversions/airvpn)](https://pypi.org/project/airvpn/)
[![PyPI version](https://img.shields.io/pypi/v/airvpn)](https://pypi.org/project/airvpn/)
[![License](https://img.shields.io/pypi/l/airvpn)](https://github.com/ch0nker/airvpn/blob/main/LICENSE)
[![Tests](https://github.com/ch0nker/airvpn/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ch0nker/airvpn/actions/workflows/python-tests.yml)

> **Note:** The docstrings and documentation was generated with AI. If you spot any errors I haven't caught yet, please open a PR or an issue.

A Python wrapper for AirVPN's [API](https://airvpn.org/apisettings/).

## Guide
- [Changelog](docs/CHANGELOG.md)
- [Contributing](docs/CONTRIBUTING.md)
- [Example](#example)
- [API Documentation](docs/api/README.md)
- [Test Documentation](docs/tests/README.md)

## Installation

PyPI:
```bash
pip install airvpn
```

Locally:
```bash
git clone https://github.com/ch0nker/airvpn.git
pip install -e airvpn
```

## Example

### Client:
```py
from airvpn.client import AirClient
from dotenv import load_dotenv

import os

load_dotenv()

client = AirClient()

user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

print(user.login)
```

### API:
Without an API key:
```py
from airvpn import AirVPN

api = AirVPN()

for server in api.status.servers:
    print(server.public_name)
```

With an API key:
```py
from airvpn import AirVPN
from dotenv import load_dotenv

import os

load_dotenv()
# Get your API key from https://airvpn.org/apisettings/
api = AirVPN(os.getenv("API_KEY"))
device = api.devices.get("test", create=True)

api.generator.download("AirVPN-Earth.conf", "earth", device.id)
```
# Python AirVPN

[![Python versions](https://img.shields.io/pypi/pyversions/airvpn)](https://pypi.org/project/airvpn/)
[![PyPI version](https://img.shields.io/pypi/v/airvpn)](https://pypi.org/project/airvpn/)
[![License](https://img.shields.io/pypi/l/airvpn)](https://github.com/ch0nker/airvpn/blob/main/LICENSE)
[![Tests](https://github.com/ch0nker/airvpn/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ch0nker/airvpn/actions/workflows/python-tests.yml)

A Python wrapper for AirVPN's [API](https://airvpn.org/apisettings/) — manage devices, generate configs, check server status, and authenticate against AirVPN's bootstrap and web services.

> **Note:** Docstrings and documentation were AI-assisted. If you spot any errors, please open a PR or an issue.

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

## Interfaces

This library exposes three interfaces depending on how much control you need:

- **`AirVPN`** — high-level wrapper, best for most use cases
- **`AirClient`** — low-level client for the encrypted bootstrap API (servers, manifest, status)
- **`WebClient`** — client for AirVPN's website/session-based endpoints (account/profile actions)

## Quick Start

### AirVPN

Without an API key (limited to public endpoints like server status):
```python
from airvpn import AirVPN

api = AirVPN()

for server in api.status.servers:
    print(server.public_name)
```

With an API key (required for account-specific actions like devices and config generation):
```python
import os

from dotenv import load_dotenv
load_dotenv()

from airvpn import AirVPN

# Get your API key from https://airvpn.org/apisettings/
api = AirVPN(os.getenv("API_KEY"))
device = api.devices.get("test", create=True)

api.generator.download("config-directory", "earth", device.id)
```

### AirClient

Without credentials:
```python
from airvpn import AirClient

client = AirClient()
manifest = client.manifest()

print(manifest.time)
```

With credentials:
```python
import os

from dotenv import load_dotenv
load_dotenv()

from airvpn import AirClient

client = AirClient()
user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

print(user.login)
```

### WebClient
```python
import os

from dotenv import load_dotenv
load_dotenv()

from airvpn import WebClient

client = WebClient()
user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

print(user.name, user.id)
```
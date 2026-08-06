# Python AirVPN

[![Python versions](https://img.shields.io/pypi/pyversions/airvpn)](https://pypi.org/project/airvpn/)
[![PyPI version](https://img.shields.io/pypi/v/airvpn)](https://pypi.org/project/airvpn/)
[![License](https://img.shields.io/pypi/l/airvpn)](https://github.com/ch0nker/airvpn/blob/main/LICENSE)
[![Tests](https://github.com/ch0nker/airvpn/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ch0nker/airvpn/actions/workflows/python-tests.yml)

A Python wrapper for AirVPN's [API](https://airvpn.org/apisettings/), covering the bootstrap, web, and REST layers of the service — authenticate, manage devices, generate configs, and check server status without touching cookies, sessions, or encryption yourself.

> **Note:** Docstrings and documentation were AI-assisted. If you spot any errors, please open a PR or an issue.

## Installation

From PyPI:
```bash
pip install airvpn
```

From source:
```bash
git clone https://github.com/ch0nker/airvpn.git
pip install -e airvpn
```

## Interfaces

The library exposes three interfaces, depending on how much control you need:

- **`AirVPN`** — high-level wrapper; the best starting point for most use cases
- **`AirClient`** — low-level client for the encrypted bootstrap API (servers, manifest, status)
- **`WebClient`** — client for AirVPN's website/session-based endpoints (account and profile actions)

## Quick Start

### AirVPN

**Log in immediately**, by passing credentials on construction. This is the simplest path if you just want to get to work:
```python
import os

from dotenv import load_dotenv
load_dotenv()

from airvpn import AirVPN

vpn = AirVPN(os.getenv("LOGIN"), os.getenv("PASSWORD"))

# Create (or fetch) a device and download a config for it
device = vpn.api.devices.get("test", create=True)
vpn.api.generator.download("config-directory", "earth", device.id)
```

**Defer login**, if you need to construct the object before credentials are available (e.g. in a CLI or app that prompts for them later):
```python
from airvpn import AirVPN

vpn = AirVPN()

# ... later, once you have credentials ...
vpn.login(username, password)

print(vpn.client.name)
```

**Skip the web login entirely**, if you already have an API key secret saved from a previous session:
```python
import os

from dotenv import load_dotenv
load_dotenv()

from airvpn import AirVPN

vpn = AirVPN(api_key=os.getenv("API_KEY"))

device = vpn.api.devices.get("test", create=True)
```

### AirClient

An `AirVPN` instance always has a `bootstrap` client available, no login required, for public data like server manifests:
```python
from airvpn import AirVPN

vpn = AirVPN()
manifest = vpn.bootstrap.manifest()

print(manifest.time)
```
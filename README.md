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
```py
from airvpn import AirVPN

api = AirVPN(API_KEY)  # API_KEY is optional for public services like whatismyip

print(api.userinfo.login)
```
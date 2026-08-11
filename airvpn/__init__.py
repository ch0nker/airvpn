"""
Python API for interacting with AirVPN.

This module provides a set of Python interfaces for working with AirVPN's
services, covering three main components:

- AirClient: A client for AirVPN's encrypted bootstrap API, used to
retrieve server and configuration data before authentication.
- AirAPI: A wrapper around AirVPN's official REST API
(https://airvpn.org/apisettings/), used for authenticated operations
such as managing devices and API keys.
- WebClient: A client that interacts directly with the AirVPN website,
handling tasks not exposed through the official API.

"""

__title__ = "AirVPN"
__version__ = "0.2.9"
__license__ = "MIT"

__all__ = [
    "AirVPN"
]

from typing import Optional

from airvpn.api import AirAPI
from airvpn.client import AirClient
from airvpn.web import WebClient

class AirVPN:
    """
    High-level entry point for interacting with AirVPN.

    Can be constructed with credentials to log in to the website and
    initialize both `client` and `api`, or with an existing API key secret
    to initialize `api` only, without touching the website at all. Can also
    be constructed with neither, deferring authentication until `login()`
    or `init_api()` is called explicitly. When logging in with credentials,
    the account is guaranteed to have at least one API key (creating one if
    necessary), and that key is used to initialize `api` automatically.

    Args:
        username (str, optional): The AirVPN account username. If provided,
            `password` must also be provided, and the client logs in to the
            website and initializes `client` and `api` immediately.
        password (str, optional): The AirVPN account password. Required if
            `username` is provided.
        api_key (str, optional): An existing AirVPN API key secret. If
            provided (and `username`/`password` are not), used to
            initialize `api` directly. This only grants REST API access —
            it does not log in to the website, so `client` will not be set.

    Attributes:
        bootstrap (AirClient): Client for AirVPN's encrypted bootstrap API.
        web (WebClient): Client for interacting with the website.
        api (AirAPI): Authenticated client for AirVPN's official REST API.

    Example:
        ```python
         # Log in immediately, with username and password (website + REST API)
         vpn = AirVPN("myusername", "mypassword")
         vpn.web.user.api.keys
         vpn.api.devices

         # REST API access only, no website login
         vpn = AirVPN(api_key="mysecret")
         vpn.api.devices.get("my-device")

         # Defer login
         vpn = AirVPN()
         vpn.login("myusername", "mypassword")
         vpn.web.user.api.keys
        ```
    """

    def __init__(self, 
                 username: Optional[str] = None, 
                 password: Optional[str] = None,
                 remember_me: bool = False,
                 api_key: Optional[str] = None):
        self.bootstrap = AirClient()
        self.web = WebClient()

        if username is not None and password is not None:
            self.login(username, password, remember_me)

            api = self.web.user.api
            if len(api.keys) == 0:
                api.add()

            api_key = api.keys[0].secret

        self.init_api(api_key)

    def login(self, username: str, password: str, remeber_me: bool = False):
        """
        Authenticate with AirVPN and initialize the API client.

        Args:
            username (str): The AirVPN account username.
            password (str): The AirVPN account password.
        """
        self.web.login(username, password, remeber_me)

    def init_api(self, api_key: str):
        """
        Initialize the AirAPI client directly from an API key secret.

        Useful for bypassing `login()` if an API key is already known.

        Args:
            api_key (str): The AirVPN API key secret.
        """
        self.api = AirAPI(api_key)

"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠤⠴⠶⠶⢶⣶⣞⠛⠍⠉⠙⠛⠳⢦⡔⠒⠒⠢⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣯⣏⣀⠀⢀⣠⠤⠖⠚⠛⠛⠻⢷⣄⣴⡄⠀⠻⣆⠀⠀⠀⠀⠻⣿⣲⣤⣀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣿⡿⠟⠻⠶⣤⡀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣤⡀⠹⣧⠀⠀⠀⠀⠈⢿⣷⣯⠛⢯⣍⠉⠙⣶⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣄⣤⣤⣤⣤⣶⣾⣿⢿⣿⣿⣿⡿⠿⢿⣿⡿⠿⠿⠶⠤⣤⣄⣈⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠙⢳⣄⢻⣇⠀⠀⠀⢠⠀⢹⣿⡄⠀⠉⢳⡄⢸⣹⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⢿⣯⣭⣿⠿⠛⠉⠉⠀⠀⣴⠟⠉⠀⠀⠀⠀⠀⠀⠈⠉⠙⠲⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡀⠀⠀⠀⣇⠀⢿⡇⠀⠀⠀⠙⣦⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣬⣿⢁⣠⣤⣤⠤⠾⠿⠥⠤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣧⡀⠀⠀⠀⠀⠀⠀⠈⢿⡇⠀⠀⠀⠘⣇⢸⡇⠀⠀⠀⠀⠈⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣠⣤⣶⣿⠿⠟⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⡄⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠈⢻⣦⡀⠀⠀⠀⠈⣉⣧⠀⠀⠀⠀
⠀⠀⠀⢛⣛⣻⣿⠉⠹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠉⠛⠒⠀⠀⠈⣿⡆⠀⠀⠀
⠀⠀⣀⣬⣽⡟⠃⠀⠀⠙⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣄⣀⠀⠀⠀⠀⠛⡇⠀⠀⠀
⢿⣿⣯⠉⠁⠀⠀⠀⠀⠀⠀⠻⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢶⡄⠀⠀⣿⠀⠀⠀
⠘⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢯⡙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⡄⠀⣿⠀⠀⠀
⠀⢻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⡉⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⣿⡆⠀⠀
⠀⠈⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⡘⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⠀⠀⠀⠀⠀⢸⣧⠀⠀
⠀⠀⢻⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⣿⡀⠀⠀⠀⠀⠈⢿⠀⠀
⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣴⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣷⣿⡇⠀⠀⠀⠀⠀⠈⡇⠀
⠀⠀⠀⠘⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀⣽⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⠏⠀⠀⠀⠀⠀⠀⢹⠀
⠀⠀⠀⠀⠘⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠠⡇
⠀⠀⠀⠀⠀⠹⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠿⠃⠀⠀⠀⣀⣠⣤⠶⠶⠚⠛⠛⠋⠉⠉⠙⠛⠳⢶⣤⡀⠀⠀⢻
⠀⠀⠀⠀⠀⠀⠹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⡟⠋⠁⠀⠀⠀⠀⠈⠀⠀⠀⠸⡇⣶⠀⠀⠀⠙⣷⡀⠀⠀⠈
⠀⠀⠀⠀⠀⠀⠀⠙⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⣤⣄⠀⠀⠀⠀⠀⠀⠀⣿⡟⠀⠀⠀⠀⠈⣿⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⣿⣷⠀⠀⠀⠀⠀⢸⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣶⣀⠠⠀⠀⠀⠀⠀⠀⠀⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣽⠃⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⢹⣿⠀⠀⠀⠀⠀⢸⡧⠀⢠
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣶⣀⢀⠀⠀⠀⠀⠀⠀⠀⠹⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⡇⣤⠀⠀⠀⠀⠀⠀⠘⣿⡇⠀⠀⠀⠀⠀⠀⢻⣿⠀⠀⠀⠀⠀⣾⠃⢀⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣆⢀⠀⠀⠀⠀⠀⠀⠘⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⢏⢠⡞⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣧⠀⠀⠀⠀⠀⢀⠀⠙⣷⣄⠀⠀⠀⠀⠀⠀⠀⠻⣷⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡿⠋⣠⠟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠋⠙⠷⣼⣲⡇⠐⠛⢫⣄⡉⠛⣷⣄⡀⠀⠀⠀⠀⠀⠙⠿⣿⣶⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠐⠒⢒⣀⣤⡴⠟⠋⣤⡾⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠈⠙⠻⢶⣼⣿⣿⣿⣷⣤⣝⣿⣶⣤⣀⠀⠀⠀⠀⠈⠙⠛⠿⠿⣿⣶⣦⣶⣶⣴⡶⠾⠿⠛⠋⠁⣀⣤⠞⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣇⣉⣿⠷⣶⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⣴⣾⣿⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⠏⠉⠉⠛⠛⠛⠛⠛⠛⠓⠒⠒⠒⠒⠒⠒⠛⠛⠛⠋⠉⠁⠀⠈⠙⠛⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
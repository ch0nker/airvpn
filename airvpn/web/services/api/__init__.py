from airvpn.web.services.common import ClientService, WebSession
from .models import *
from airvpn.exceptions import InvalidAPIKey

from collections.abc import Callable

import time

__title__ = "API"

class APIManager(ClientService):
    """Manages the authenticated user's AirVPN API keys.

    Wraps the AJAX endpoints behind ``https://airvpn.org/apisettings/`` to
    list, add, rename, and delete API keys.

    Attributes:
        keys (list[APIKey]): All API keys currently owned by the user.
    """

    __URL__ = "https://airvpn.org/apisettings/"

    def __init__(self, session: WebSession):
        super().__init__(APIManager.__URL__, session)
        self.keys: list[APIKey] = []
        self._key_map = {}
        self.update()

    def update(self, data = None):
        """Refresh `keys` from the server manifest.

        Fetches the current manifest and repopulates `keys` and the
        internal key lookup map from the response.
        """
        data = data or self.request("manifest")
        self._key_map = {}
        self.keys = []

        for key in data.get("keys", []):
            key = APIKey(**key)
            self._key_map[key.id] = key
            self.keys.append(key)

    def poll_update(self, check_callback: Callable[[list[APIKeyDict]], bool]):
        keys = []
        data = None

        while check_callback(keys):
            data = self.request("manifest")
            keys = data.get("keys", [])
            time.sleep(7)

        self.update(data)

    def add(self) -> APIKey:
        """Create a new API key.

        The ``"add"`` action doesn't return the new key's data, so `update`
        is called afterward to refresh `keys` with the newly created key.

        Returns:
            APIKey: The most recently added api key.
        """
        self.request("add")
        self.poll_update(
            lambda keys : len(keys) - len(self.keys) < 0
        )

        return self.keys[len(self.keys) - 1]

    def get(self, key: APIKey | str):
        if isinstance(key, str):
            _key = self._key_map.get(key)
            if _key is None:
                raise InvalidAPIKey(f"No key with the id of `{key}` exists")
            key = _key

        return key

    def edit(self, key: APIKey | str, name: str):
        """Rename an existing API key.

        Args:
            key: `APIKey` instance or key ID to edit.
            name: New name to set for the key.

        Raises:
            InvalidAPIKey: If `key` is a string ID that doesn't match any
                known key.
        """
        key = self.get(key)

        key.name = name

        self.edit_request("name", name, id=key.id)

    def delete(self, key: APIKey | str):
        """Delete an existing API key.

        Args:
            key: `APIKey` instance or key ID to delete.

        Raises:
            InvalidAPIKey: If `key` is a string ID that doesn't match any
                known key.
        """
        key = self.get(key)

        self.request("delete", id=key.id)

        self.keys.remove(key)
        del self._key_map[key.id]
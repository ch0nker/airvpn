from __future__ import annotations

from airvpn.web.auth.services.common import ClientService, WebSession
from .models import DeviceKey, DeviceKeyDict

from airvpn.exceptions import ValidationError

from collections.abc import Callable

import time

class DeviceManager(ClientService):
    """Manages the authenticated user's registered devices.

    Wraps the AJAX endpoints behind ``https://airvpn.org/devices/`` to
    list, edit, renew, and delete the user's devices.

    Attributes:
        total_deprecated (int): Number of deprecated devices on the account.
        devices (list[DeviceKey]): All devices currently registered to the account.
    """
    __URL__ = "https://airvpn.org/devices/"

    def __init__(self, session: WebSession):
        super().__init__(DeviceManager.__URL__, session)
        self.total_deprecated = 0
        self.devices: list[DeviceKey] = []
        self._device_map = {}
        self.update()

    def update(self, data):
        """Refresh `devices` and `total_deprecated` from the server.

        Args:
            data: Pre-fetched manifest data to use instead of making a new
                request. If falsy, the manifest is fetched from the server.
        """
        data = data or self.request("manifest")
        self.total_deprecated = data.get("total_deprecated")

        self.devices = []
        self._device_map = {}
        for key in data.get("keys", []):
            key = DeviceKey(**key)
            self.devices.append(key)
            self._device_map[key.id] = key

    def poll_update(self, check_callback: Callable[[list[DeviceKeyDict]], bool]):
        """Poll the server until a condition is met, then refresh `devices`.

        Repeatedly fetches the device manifest, sleeping one second between
        attempts, until `check_callback` returns False for the current set
        of keys, then applies the final result via `update`.

        Args:
            check_callback: Called with the current list of raw key data on
                each poll; polling continues while it returns True.
        """
        keys = []
        data = None

        while check_callback(keys):
            data = self.session.request("manifest")
            keys = data.get("keys", [])
            time.sleep(1)

        self.update(data)

    def get(self, device: DeviceKey | str):
        """Resolve a device to a `DeviceKey` instance.

        Args:
            device: `DeviceKey` instance or device ID to resolve.

        Returns:
            The matching `DeviceKey` instance.

        Raises:
            ValidationError: If `device` is a string ID that doesn't match
                any known device.
        """
        if isinstance(device, str):
            _device = self._device_map.get(device)
            if _device is None:
                raise ValidationError(f"Failed to find the device with an id of \"{device}\"")

            device = _device

        return device

    def edit(self,
             device: DeviceKey | str,
             name: str | None = None,
             description: str | None = None):
        """Edit a device's name and/or description.

        Args:
            device: `DeviceKey` instance or device ID to edit.
            name: New name to set for the device, if any.
            description: New description to set for the device, if any.

        Raises:
            ValidationError: If neither `name` nor `description` is provided.
        """
        device = self.get(device)

        if name is None and description is None:
            raise ValidationError("You need either need to set a new name or description to edit devices.")

        if name is not None:
            self.edit_request("name", name, id=device.id)
            device.name = name

        if description is not None:
            self.edit_request("description", description, id=device.id)
            device.description = description

    def add(self):
        """Register a new device and refresh `devices` once it appears."""
        self.request("add")
        self.poll_update(
            lambda keys : len(keys) - len(self.keys) < 0
        )

    def renew(self, device: DeviceKey | str):
        """Renew an existing device.

        Args:
            device: `DeviceKey` instance or device ID to renew.
        """
        device = self.get(device)
        self.request("renew", id=device.id)

    def delete(self, device: DeviceKey | str):
        """Delete an existing device.

        Args:
            device: `DeviceKey` instance or device ID to delete.
        """
        device = self.get(device)

        self.request("delete", id=device.id)

        self.devices.remove(device)
        del self._device_map[device.id]
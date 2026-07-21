from airvpn.network import AirSession
from airvpn.exceptions import DeviceAPIError, DeviceValidationError
from airvpn.devices.models import Device

from enum import StrEnum

class DeviceAction(StrEnum):
    """Actions available for managing devices via the devices endpoint."""
    LIST = "list"
    ADD = "add"
    DELETE = "delete"
    MODIFY = "modify"
    RENEW = "renew"

class Devices:
    """
    Manages registered devices/keys associated with the account.
    
    Attributes:
        devices: A list of devices

    Access type:
        User-specific, API KEY required
    """

    __KEY_NEEDED__ = True

    def __init__(self, session: AirSession):
        self.session = session
        self._diff = False
        self._devices: list[Device] = []
        self._device_map: dict[str, Device] = {}
    
    def action(self,
               action: DeviceAction,
               id: str | None = None,
               name: str | None = None,
               description: str | None = None):
        """Send a raw devices action request.

        Args:
            action: The device action to perform.
            id: The device's ID. Required for delete, renew, and modify.
            name: The device's name. Used for add and modify.
            description: The device's description. Used for add and modify.

        Returns:
            The parsed JSON response from the devices endpoint.

        Raises:
            DeviceException: If the response contains an error.
        """

        result = self.session.get("devices", params={
            "action": action, "id": id, "name": name, "description": description
        }).json()

        error = result.get("error", None)
        if error is not None:
            raise DeviceAPIError(error)

        return result
    
    def _cache_devices(self):
        self._devices = []
        self._device_map = {}

        self._devices = self.list()
        for device in self._devices:
            self._device_map[device.name] = device
    
    def _update_diff(self):
        if self._diff or not self._devices:
            self._cache_devices()
            self._diff = False

    def get(self, name: str, create: bool = False):
        """Get/create a device using a name
        
        Args:
            name: Name to search for.
            create: If it cannot find the device it will create it.

        Returns:
            The Device object or None
        """
        # TODO: Possibly create devices locally since this is an amount of requests I'd rather not have.
    
        self._update_diff()
        result = self._device_map.get(name)

        if not result and create:
            device_id = self.add()

            if device_id is None:
                raise DeviceValidationError("Failed to create device")
            if not self.modify(device_id, name):
                raise DeviceValidationError("Failed to modify device's name")

            self._update_diff()
            result = self._device_map.get(name)

        return result

    @property
    def devices(self):
        """A list of Devices."""

        if self._devices:
            self._update_diff()

            return self._devices

        self._cache_devices()

        return self._devices
    
    def list(self):
        """List all devices registered to the account.

        Returns:
            A list of Device objects.
        """
        response = self.action(DeviceAction.LIST)

        return [Device(**device) for device in response.get("devices", [])]
    
    def add(self):
        """Register a new device.

        Returns:
            The ID of the newly created device, or None if not returned.
        """
        response = self.action(DeviceAction.ADD)

        self._diff = True

        return response.get("id", None)
    
    def delete(self, id: str):
        """Delete a device.

        Args:
            id: The ID of the device to delete.

        Returns:
            True if successful in deleting the device.
        """
        response = self.action(DeviceAction.DELETE, id=id)

        self._diff = True

        return response.get("result", "error") == "ok"
    
    def renew(self, id: str):
        """Renew a device.

        Args:
            id: The ID of the device to renew.

        Returns:
            True if successful in renewing the device.
        """
        response = self.action(DeviceAction.RENEW, id=id)

        self._diff = True

        return response.get("result", "error") == "ok"

    def modify(self, id: str, name: str | None = None, description: str | None = None):
        """Modify a device's name and/or description.

        Args:
            id: The ID of the device to modify.
            name: The new name for the device, if changing it.
            description: The new description for the device, if changing it.

        Returns:
            True if successful in modifying the device.

        Raises:
            DeviceException: If neither name nor description is provided.
        """
        if name is not None and description is not None:
            raise DeviceValidationError("You either need to modify name or description.")

        response = self.action(DeviceAction.MODIFY, id=id, name=name, description=description)

        self._diff = True
        
        return response.get("result", "error") == "ok"
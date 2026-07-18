from airvpn.network import AirSession, Status
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
    
    Access type:
        User-specific, API KEY required
    """

    KEY_NEEDED = True

    def __init__(self, session: AirSession):
        self.session = session
    
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
            AssertionError: If the response contains an error.

        """

        result = self.session.get("devices", params={
            "action": action, "id": id, "name": name, "description": description
        }).json()

        error = result.get("error", None)
        assert not error, error

        return result

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

        return response.get("id", None)
    
    def delete(self, id: str):
        """Delete a device.

        Args:
            id: The ID of the device to delete.

        Returns:
            True if successful in deleting the device.
        """

        response = self.action(DeviceAction.DELETE, id=id)

        return response.get("result", "error") == "ok"
    
    def renew(self, id: str):
        """Renew a device.

        Args:
            id: The ID of the device to renew.

        Returns:
            True if successful in renewing the device.
        """

        response = self.action(DeviceAction.RENEW, id=id)

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
            AssertionError: If neither name nor description is provided.
        """
        assert name is not None or description is not None, "You either need to modify name or description."

        response = self.action(DeviceAction.MODIFY, id=id, name=name, description=description)
        
        return response.get("result", "error") == "ok"
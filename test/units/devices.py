import os

from airvpn import AirVPN

api = AirVPN(os.getenv("API_KEY"))
devices = None
device_id = None

@test.unit
def check_service():
    global devices
    devices = api.devices

@test.unit
def add_device():
    global device_id
    device_id = devices.add()
    assert device_id, "Failed to create device"
    print(f"Testing with device id: {device_id}")

@test.unit
def modify_device():
    assert devices.modify(device_id, "API Test", "Description for testing"), "Failed to modify device"

@test.unit
def renew_device():
    assert devices.renew(device_id), "Failed to renew device"

@test.unit
def list_devices():
    for device in devices.list():
        print(device.name, device.description)

@test.unit
def delete_device():
    assert devices.delete(device_id), "Failed to delete device"
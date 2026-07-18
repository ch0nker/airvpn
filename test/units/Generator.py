import os
import json

from airvpn import AirVPN

airvpn = AirVPN(os.getenv("API_KEY"))
generator = None
devices = None

@test.unit
def check_request():
    global generator, devices

    generator = airvpn.generator
    devices = airvpn.devices
    
    assert generator, "Failed to get generator service"
    assert devices, "Failed to get devices service"

@test.unit
def generate():
    device_list = devices.list()

    assert device_list, "Empty device list"

    device = device_list[0]
    config = generator.create_config("ross", device.name)

    assert config, "Failed to receive config"
    
    try:
        data = json.loads(config)
        message = data.get("error")
        print(data)
        assert message, "Failed to receive error, most likely a multi-config generation."
        raise Exception(message)
    except json.JSONDecodeError:
        assert len(config) > 0, "Config length is 0"
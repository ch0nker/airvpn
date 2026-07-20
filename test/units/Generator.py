import os

from shutil import rmtree
from airvpn import AirVPN
from airvpn.generator import ProtocolType, VpnType

airvpn = AirVPN(os.getenv("API_KEY"))
generator = None
devices = None
device_name = None

@test.unit
def check_request():
    global generator, devices

    generator = airvpn.generator
    devices = airvpn.devices
    
    assert generator, "Failed to get generator service"
    assert devices, "Failed to get devices service"

@test.unit
def generate():
    global device_name
    device_list = devices.list()

    assert device_list, "Empty device list"

    device = device_list[0]
    device_name = device.name
    config = generator.create_config("ross", device_name)

    assert config, "Failed to receive config"
    assert len(config) > 0, "Config length is 0"

@test.unit
def write():
    assert device_name, "No device name"

    servers = ["earth", "caelum", "castula", "alrai"]
    generator.write_config("config", servers, device_name)

    assert os.path.exists("config") or os.listdir("config") == len(servers), "Failed to write configs"
    rmtree("config")

@test.unit
def batch_generate():
    assert device_name, "No device name"

    servers = ["earth", "caelum", "castula", "alrai"]
    configs = generator.create_config(servers, device_name)
    for config in configs:
        config.write("config")

    assert os.path.exists("config") or os.listdir("config") == len(configs), "Failed to write configs"
    rmtree("config")

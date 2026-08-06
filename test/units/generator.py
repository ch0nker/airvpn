import os

from shutil import rmtree
from airvpn import AirVPN

airvpn = AirVPN(api_key=os.getenv("API_KEY"))
generator = None
devices = None
device_name = None

@test.unit
def check_request():
    print("Caching services.")
    global generator, devices

    generator = airvpn.api.generator
    devices = airvpn.api.devices
    
    assert generator, "Failed to get generator service"
    assert devices, "Failed to get devices service"
    print("Finished.")

@test.unit
def generate():
    print("Generating a single config.")
    global device_name
    device_list = devices.list()

    assert device_list, "Empty device list"

    device = device_list[0]
    device_name = device.name
    config = generator.create("ross", device_name)

    assert config, "Failed to receive config"
    assert len(config) > 0, "Config length is 0"
    print("Finished.")

@test.unit
def write():
    print("Writing configs to disk.")
    assert device_name, "No device name"

    servers = ["earth", "caelum", "castula", "alrai"]
    generator.download("config", servers, device_name)

    assert os.path.exists("config") or os.listdir("config") == len(servers), "Failed to write configs"
    rmtree("config")

    print("Finished.")

@test.unit
def batch_generate():
    print("Creating multiple configs")
    assert device_name, "No device name"

    servers = ["earth", "caelum", "castula", "alrai"]
    configs = generator.create(servers, device_name)
    print("Writing configs to disk.")
    for config in configs:
        config.write("config")

    assert os.path.exists("config") or os.listdir("config") == len(configs), "Failed to write configs"
    rmtree("config")
    print("Finished.")

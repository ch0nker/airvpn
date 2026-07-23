import os

from airvpn.client import AirClient


client: AirClient = None

@test.unit
def get_client():
    global client
    client = AirClient()

@test.unit
def get_manifest():
    assert client, "Failed to get client"

    manifest = client.manifest()

    assert manifest, "Failed to get manifest"

@test.unit
def get_user():
    assert client, "Failed to get client"

    user = client.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))

    assert user, "Failed to get user"
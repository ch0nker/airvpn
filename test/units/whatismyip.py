from airvpn import AirVPN

api = AirVPN()
whatismyip = None

@test.unit
def check_service():
    print("Caching service.")
    global whatismyip
    whatismyip = api.api.whatismyip

@test.unit
def check_fetch():
    print("Fetching ip information.")
    info = whatismyip.fetch()

    assert info.ip, "Failed to get ip"
    assert info.geo, "Failed to get geo object"
    assert info.geo_additional, "Failed to get geo_additional object"

    print("Finished.")

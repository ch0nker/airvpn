from airvpn import AirVPN

api = AirVPN()
whatismyip = None

@test.unit
def check_service():
    global whatismyip
    whatismyip = api.whatismyip

@test.unit
def check_fetch():
    info = whatismyip.fetch()

    print(info.ip, info.geo_additional.continent_name, info.geo_additional.country_name, info.geo_additional.region_name)

from airvpn import AirVPN

api = AirVPN()
status = None

@test.unit
def check_service():
    global status
    status = api.status

@test.unit
def list_servers():
    assert status.servers, "Empty servers list"
    for server in status.servers[:10]:
        print("Server:", server.public_name, server.country_code)

@test.unit
def list_countries():
    assert status.servers, "Empty countries list"
    for country in status.countries[:10]:
        print("Country:", country.country_name, country.country_code)

@test.unit
def list_continents():
    assert status.servers, "Empty continents list"
    for continent in status.continents:
        print("Continent:", continent.public_name)

@test.unit
def list_planets():
    assert status.servers, "Empty planets list"
    for planet in status.planets:
        print("Planet:", planet.public_name)

@test.unit
def list_routing():
    assert status.servers, "Empty routing list"
    for routing in status.routing[:5]:
        print("Routing:", routing.public_name, routing.country_code)


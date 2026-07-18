from airvpn import AirVPN

api = AirVPN()
status = None

@test.unit
def check_service():
    global status
    status = api.status

@test.unit
def list_servers():
    for server in status.servers[:10]:
        print("Server:", server.public_name, server.country_code)

@test.unit
def list_countries():
    for country in status.countries[:10]:
        print("Country:", country.country_name, country.country_code)

@test.unit
def list_continents():
    for continent in status.continents:
        print("Continent:", continent.public_name)

@test.unit
def list_planets():
    for planet in status.planets:
        print("Planet:", planet.public_name)

@test.unit
def list_routing():
    for routing in status.routing[:5]:
        print("Routing:", routing.public_name, routing.country_code)


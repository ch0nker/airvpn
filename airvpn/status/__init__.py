from airvpn.network import AirSession, Status as NetworkStatus
from airvpn.status.models import Routing, Server, Country, Continent, Planet

class Status:
    """Represents the full VPN network status response.

    Attributes:
        servers: List of individual VPN servers and their current status.
        routing: List of routing nodes and their current status.
        countries: List of aggregate VPN status per country.
        continents: List of aggregate VPN status per continent.
        planets: List of aggregate VPN status globally (typically a single entry).
        deprecated_warning: A warning about deprecated fields in the response,
            if present; otherwise None.
        result: A status message from network.Status indicating whether the
            overall request succeeded.

    Access type:
        Public, no API KEY required.
    """

    __KEY_NEEDED__ = False

    def __init__(self, session: AirSession):
        response = session.get("status")
        response_json = response.json()

        self.servers = [Server(**server) for server in response_json.get("servers", [])]
        self.routing = [Routing(**routing) for routing in response_json.get("routing", [])]
        self.countries = [Country(**country) for country in response_json.get("countries", [])]
        self.continents = [Continent(**continent) for continent in response_json.get("continents", [])]
        self.planets = [Planet(**planet) for planet in response_json.get("planets", [])]

        self.deprecated_warning: str | None = response_json.get("deprecated_warning", None)
        self.result = NetworkStatus(response_json.get("result"))
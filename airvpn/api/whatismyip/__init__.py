from airvpn.api.network import AirSession
from airvpn.api.whatismyip.models import IpInfo

__title__ = "WhatIsMyIp"

class WhatIsMyIp:
    """Your IP address, and a check if you are reaching API from our VPN or not.

    Access type:
        Public, no API KEY required.
    """

    __KEY_NEEDED__ = False

    def __init__(self, session: AirSession):
        self.session = session

    def fetch(self) -> IpInfo:
        """Fetch the current IP address and geolocation info.

        Returns:
            An IpInfo object containing the detected IP, IP version flags, AirVPN status, and geolocation details.

        Raises:
            RateLimited: If too many requests go through.
            APIError: If the request results in an error.
        """
        json = self.session.service_request("get", "whatismyip")

        return IpInfo(**json)
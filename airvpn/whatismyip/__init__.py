from airvpn.network import AirSession
from airvpn.whatismyip.models import IpInfo

class WhatIsMyIp:
    """Your IP address, and a check if you are reaching API from our VPN or not.

    Access type:
        Public, no API KEY required.
    """

    __KEY_NEEDED__ = False

    def __init__(self, session: AirSession):
        self.session = session

    def fetch(self):
        """Fetch the current IP address and geolocation info.

        Returns:
            An IpInfo object containing the detected IP, IP version flags,
            AirVPN status, and geolocation details.
        """
        response = self.session.get("whatismyip")

        return IpInfo(**response.json())
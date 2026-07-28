"""
I can't really understand the documentation for dns_lists.

If you can understand it or can get it to change at all please open an issue or create a PR with how you did it.
"""

__title__ = "DnsLists"

from airvpn.api.network import AirSession
from airvpn.api.dns_lists.models import Dns

class DnsLists:
    """Fetches available DNS filtering lists.

    Access type:
        Public, no API KEY required

    Attributes:
        lists: A dict mapping list keys to their corresponding Dns objects.
    """

    __KEY_NEEDED__ = False

    def __init__(self, session: AirSession):
        json = session.service_request("get", "dns_lists")

        self.lists: dict[str, Dns] = {}

        for key, dns in json.get("lists", {}).items():
            self.lists[key] = Dns(**dns)
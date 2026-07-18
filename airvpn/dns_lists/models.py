from typing import Unpack, TypedDict

class DnsDict(TypedDict, total=False):
    name: str
    description: str
    home: str | None
    last_update_unix: int
    n_items: int

class Dns:
    """Represents a DNS filtering list/profile.

    Attributes:
        name: The DNS list's name.
        description: Description of the DNS list.
        home: URL of the DNS list's home page/source, if available;
            otherwise None.
        last_update_unix: Unix timestamp of when the DNS list was last updated.
        n_items: Number of entries in the DNS list.
    """
    def __init__(self, **kwargs: Unpack[DnsDict]):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.home = kwargs.get("home")
        self.last_update_unix = kwargs.get("last_update_unix")
        self.n_items = kwargs.get("n_items")
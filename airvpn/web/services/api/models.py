from typing import TypedDict, Unpack
from datetime import datetime, timezone


class APIKeyDict(TypedDict, total=False):
    id: str
    color: str
    name: str
    secret_short: str
    secret: str
    creation_date: int

class APIKey:
    """An AirVPN API key belonging to the authenticated user.

    Constructed from the key entries returned by the `APIManager`
    manifest.

    Attributes:
        id (str | None): Unique identifier of the key.
        color (str | None): CSS color assigned to the key for display
            purposes, as an HSL string (e.g. ``"hsl(68,80%,87.5%)"``).
        name (str | None): Display name of the key.
        secret_short (str | None): Truncated/masked preview of the key's
            secret, safe for display.
        secret (str | None): The key's full secret value.
        creation_date (datetime): UTC timestamp of when the key was
            created, converted from the manifest's Unix timestamp.
    """
    def __init__(self, **kwargs: Unpack[APIKeyDict]):
        self.id = kwargs.get("id")
        self.color = kwargs.get("color")
        self.name = kwargs.get("name")
        self.secret_short = kwargs.get("secret_short")
        self.secret = kwargs.get("secret")
        self.creation_date = datetime.fromtimestamp(kwargs.get("creation_date"), tz=timezone.utc)

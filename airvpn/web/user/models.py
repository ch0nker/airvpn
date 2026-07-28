from typing import TypedDict, Unpack
from datetime import datetime

class RankDict(TypedDict):
    name: str
    level: int


class Rank:
    """Represents a forum rank/title assigned to a user.

    Attributes:
        name (str | None): Display name of the rank.
        level (int | None): Numeric level of the rank.
    """

    def __init__(self, **kwargs: Unpack[RankDict]):
        self.name = kwargs.get("name")
        self.level = kwargs.get("level")


class AboutDict(TypedDict, total=False):
    rank: Rank
    birthday: datetime

class About:
    """Represents the "About" section of a user's profile.

    Attributes:
        rank (Rank | None): The user's rank.
        birthday (str | None): The user's birthday, if disclosed.
    """

    def __init__(self, **kwargs: Unpack[AboutDict]):
        self.rank = kwargs.get("rank")
        self.birthday = kwargs.get("birthday")

class ContactsDict(TypedDict, total=False):
    website: str
    twitter: str
    mastodon: str
    aim: str
    msn: str
    icq: str
    yahoo: str
    xmpp: str
    skype: str

class Contacts:
    def __init__(self, **kwargs: Unpack[ContactsDict]):
        self.website = kwargs.get("website", "")
        self.twitter = kwargs.get("twitter", "")
        self.mastodon = kwargs.get("mastodon", "")
        self.aim = kwargs.get("aim", "")
        self.msn = kwargs.get("msn", "")
        self.icq = kwargs.get("icq", "")
        self.yahoo = kwargs.get("yahoo", "")
        self.xmpp = kwargs.get("xmpp", "")
        self.skype = kwargs.get("skype", "")

class WebUserDict(TypedDict, total=False):
    name: str
    id: int
    image: str
    content_count: int
    followers: int
    community_reputation: int
    last_visited: datetime
    joined: datetime
    days_won: int
    contacts: Contacts
    rank: str
    about: About
    gender: str
    location: str
    interests: str
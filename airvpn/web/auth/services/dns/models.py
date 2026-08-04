from typing import TypedDict, Unpack, Literal
from datetime import datetime, timezone

from enum import StrEnum

class AnswerType(StrEnum):
    EXACT = "exact"
    DOMAIN = "domain"
    CONTAIN = "contain"
    WILDCARD = "wildcard"
    STARTS_WITH = "startswith"
    ENDS_WITH = "endswith"

class ActionType(StrEnum):
    DENY = "deny"
    ALLOW = "allow"
    CUSTOM = "custom"

class RecordType(StrEnum):
    A = "A"
    AAAA = "AAAA"
    TXT = "TXT"
    CNAME = "CNAME"

class RecordDict(TypedDict):
    type: RecordType
    value: str

class Record:
    def __init__(self, **kwargs: Unpack[RecordDict]):
        self.type = kwargs.get("type")
        self.value = kwargs.get("value")

    def to_json(self) -> RecordDict:
        return {
            "type": self.type,
            "value": self.value
        }

class AnswerDict(TypedDict):
    type: AnswerType
    host: str
    action: ActionType
    records: list[RecordDict]

class Answer:
    def __init__(self, **kwargs: Unpack[AnswerDict]):
        self.type = kwargs.get("type")
        self.host = kwargs.get("host")
        self.action = kwargs.get("action")
        self.records = [Record(**record) for record in kwargs.get("records", [])]

    def to_json(self) -> AnswerDict:
        return {
            "type": self.type,
            "host": self.host,
            "aciton": self.action,
            "records": [record.to_json() for record in self.records]
        }

class CurrentDict(TypedDict):
    lists: list[str]
    custom: bool
    answers: list[AnswerDict]
    hole: Literal["default", "invalid", "page", "localhost", "nxdomain", "none"]
    routingtable: Literal["default", "general", "none"]
    useapplicationdnsdotnet: Literal["default", "nxdomain", "none"]

class Current:
    """The user's currently active custom DNS configuration.

    Attributes:
        lists (list[str]): Codes of the DNS lists currently selected.
        enabled (bool): Whether custom DNS is currently enabled.
    """
    def __init__(self, **kwargs: Unpack[CurrentDict]):
        self.lists = kwargs.get("lists")
        self.enabled = kwargs.get("custom")
        self.answers = [Answer(**answer) for answer in kwargs.get("answers", [])]
        self.hole = kwargs.get("hole")
        self.routing_table = kwargs.get("routingtable")
        self.use_application_dns_dot_net = kwargs.get("useapplicationdnsdotnet")

    def to_json(self) -> CurrentDict:
        return {
            "lists": self.lists,
            "custom": self.enabled,
            "answers": [answer.to_json() for answer in self.answers],
            "hole": self.hole,
            "routingtable": self.routing_table,
            "useapplicationdnsdotnet": self.use_application_dns_dot_net
        }

class DnsListDict(TypedDict, total=False):
    code: str
    name: str
    description: str | None
    home: str
    experimental: bool
    nitems: int
    last_update: int

class DnsList:
    """A DNS list available from AirVPN.

    Attributes:
        code (str): Unique code identifying the DNS list.
        name (str): Display name of the DNS list.
        description (str | None): Optional free-text description of the list.
        home (str): Homepage URL associated with the list.
        experimental (bool): Whether the list is marked experimental.
        nitems (int): Number of entries contained in the list.
        last_update (datetime): UTC timestamp of when the list was last updated.
    """
    def __init__(self, **kwargs: Unpack[DnsListDict]):
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.home = kwargs.get("home")
        self.experimental = kwargs.get("experimental")
        self.nitems = kwargs.get("nitems")
        self.last_update = datetime.fromtimestamp(kwargs.get("last_update", 0), timezone.utc)
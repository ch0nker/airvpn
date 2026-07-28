from airvpn.api.network import AirSession
from airvpn.api.userinfo.models import Connection, User

__title__ = "UserInfo"

class UserInfo:
    """Details about yourself, including connection details.

    Access type:
        User-specific, API KEY required.

    Attributes:
        user: Info about the account that generated the API key.
        sessions: A list of connections ordered oldest to newest.
        connection: Info about the oldest connection.
    """

    __KEY_NEEDED__ = True

    def __init__(self, session: AirSession):
        json = session.service_request("get", "userinfo")
        
        self.user = User(**json.get("user", {}))
        self.sessions = [Connection(**s) for s in json.get("sessions", [])]
        self.connection = Connection(**json.get("connection", {}))
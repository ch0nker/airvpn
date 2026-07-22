from airvpn.network import AirSession, AirStatus
from airvpn.userinfo.models import Connection, User

class UserInfo:
    """Details about yourself, including connection details.

    Attributes:
        user: Info about the account that generated the API key.
        sessions: A list of connections ordered oldest to newest.
        connection: Info about the oldest connection.

    Access type:
        User-specific, API KEY required.
    """

    __KEY_NEEDED__ = True

    def __init__(self, session: AirSession):
        json = session.service_request("get", "userinfo")
        
        self.user = User(**json.get("user", {}))
        self.sessions = [Connection(**s) for s in json.get("sessions", [])]
        self.connection = Connection(**json.get("connection", {}))
from airvpn.network import AirSession, Status
from airvpn.userinfo.models import Connection, User

class UserInfo:
    """Details about yourself, including connection details.

    Attributes:
        user: Info about the account that generated the API key.
        sessions: A list of connections ordered oldest to newest.
        connection: Info about the oldest connection.
        result: A status message from network.Status.

    Access type:
        User-specific, API KEY required.
    """

    KEY_NEEDED = True

    def __init__(self, session: AirSession):
        response = session.get("userinfo")
        response_json = response.json()
        
        self.user = User(**response_json.get("user", {}))
        self.sessions = [Connection(**s) for s in response_json.get("sessions", [])]
        self.connection = Connection(**response_json.get("connection", {}))

        self.result = Status(response_json.get("result", "warning"))
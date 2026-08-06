from airvpn.web.auth.services.common import ClientService, WebSession
from .models import Session

class SessionManager(ClientService):
    """Manages the authenticated user's active VPN sessions.

    Wraps the AJAX endpoints behind ``https://airvpn.org/sessions/`` to
    list the user's currently active sessions.

    Attributes:
        sessions (list[Session]): All sessions currently active on the account.
    """

    __URL__ = "https://airvpn.org/sessions/"

    def __init__(self, session: WebSession):
        super().__init__(SessionManager.__URL__, session)
        self.sessions: list[Session] = []
        self.update()

    def update(self):
        """Refresh `sessions` from the server manifest."""
        data = self.request("manifest")
        self.sessions = [Session(**session) for session in data.get("sessions", [])]
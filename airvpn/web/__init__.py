from airvpn.web.auth import AuthUser

__title__ = "WebClient"

class WebClient:
    """High-level entry point for interacting with the AirVPN website.

    Attributes:
        user (AuthUser | None): The currently authenticated user, or ``None``
            if `login` has not yet been called.
    """

    def __init__(self):
        self.user = None

    def login(self, username: str, password: str) -> AuthUser:
        """Authenticate with the AirVPN website.

        Args:
            username: Account username or email address.
            password: Account password.

        Returns:
            The authenticated user, also stored on ``self.user``.

        Raises:
            LoginError: If authentication fails.
        """
        self.user = AuthUser(username, password)

        return self.user
"""An interface for interacting with the website."""

from __future__ import annotations

from typing import Optional

from .network import WebSession

from .user import WebUser
from .auth import AuthUser
from .forum import ForumManager

__title__ = "WebClient"

class WebClient:
    """High-level entry point for interacting with the AirVPN website.

    Attributes:
        user (AuthUser | None): The currently authenticated user, or ``None``
            if `login` has not yet been called.
        session (WebSession): The underlying session used for all requests.
        forum (ForumManager): Entry point for browsing the site's forums.
    """

    def __init__(self):
        self.user = None
        self.session = WebSession()
        self.forum = ForumManager(self.session)

    def find_member(self, username: str) -> list[WebUser]:
        """Search for members by username.

        Args:
            username: Full or partial username to search for.

        Returns:
            Matching users found by the search.
        """
        data = self.session.ajax("get", "findMember", "ajax", ajax_params={
            "input": username
        }).json()

        return [WebUser(
            self.session,
            name=user.get("name"),
            id=int(user.get("id")),
            image=user.get("photo")
        ) for user in data]

    def login(self,
              username: Optional[str] = None, password: Optional[str] = None,
              remember_me: bool = False, session_key: Optional[str] = None) -> AuthUser:
        """Authenticate with the AirVPN website.

        Args:
            username(str): Account username or email address.
            password(str): Account password.
            remember_me(bool): Store the session credentials in keyring.
            session_key(str): Session key from `AuthUser.get_sesion_key()`.

        Returns:
            The authenticated user, also stored on ``self.user``.

        Raises:
            LoginError: If authentication fails.
        """
        self.user = AuthUser(username, password, self.session, remember_me, session_key)

        return self.user
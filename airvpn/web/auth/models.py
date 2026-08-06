"""Data models for AirVPN web authentication.

Re-exports models from client services modules under `airvpn.web.auth.services`,
and defines enums used when interacting with the authenticated user's account
(e.g. profile privacy settings).
"""

from datetime import datetime, timezone

from typing import TypedDict, Unpack

from enum import IntEnum

class BaseNotificationDict(TypedDict, total=False):
    id: str
    title: str
    url: str
    date: str
    author_photo: str

class BaseNotification:
    def __init__(self, **kwargs: Unpack[BaseNotificationDict]):
        self.id = int(kwargs.get("id"))
        self.title = kwargs.get("title")
        self.url = kwargs.get("url")
        self.date = datetime.fromtimestamp(int(kwargs.get("date")), timezone.utc)
        self.author_photo = kwargs.get("author_photo")


class NotificationDict(BaseNotificationDict):
    content: str

class Notification(BaseNotification):
    def __init__(self, **kwargs: Unpack[NotificationDict]):
        super().__init__(**kwargs)
        self.content = kwargs.get("content")

class MessageDict(BaseNotificationDict):
    message: str

class Message(BaseNotification):
    def __init__(self, **kwargs: Unpack[MessageDict]):
        super().__init__(**kwargs)
        self.message = kwargs.get("message")

class ProfilePrivacy(IntEnum):
    """Controls who is allowed to view a user's profile.

    Used with `AuthUser.edit_profile` to set the
    `air_ipb_profile_privacy_title` field on the profile edit form.

    Attributes:
        ALL: Profile is visible to everyone, including guests.
        FOLLOWED_MEMBERS: Profile is visible only to members the user follows.
        COMMUNITY_MEMBERS: Profile is visible only to registered/logged-in
            community members.
        PRIVATE: Profile is visible only to the user themselves.
    """
    ALL = 1
    FOLLOWED_MEMBERS = 2
    COMMUNITY_MEMBERS = 3
    PRIVATE = 4
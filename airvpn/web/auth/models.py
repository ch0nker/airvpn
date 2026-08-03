"""Data models for AirVPN web authentication.

Re-exports models from client services modules under `airvpn.web.auth.services`,
and defines enums used when interacting with the authenticated user's account
(e.g. profile privacy settings).
"""

from enum import IntEnum

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
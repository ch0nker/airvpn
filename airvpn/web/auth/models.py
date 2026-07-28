from enum import IntEnum

class ProfilePrivacy(IntEnum):
    ALL = 1
    FOLLOWED_MEMBERS = 2
    COMMUNITY_MEMBERS = 3
    PRIVATE = 4
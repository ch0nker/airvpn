from airvpn.web.user.models import WebUserDict, About, Rank, Contacts
from airvpn.web.network import WebSession
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Unpack

import re
import time

class WebUser:
    """Represents an AirVPN forum member's public profile.

    Fields passed in via ``kwargs`` are used directly; any field not
    supplied is lazily fetched (and cached) by scraping the user's profile
    page the first time it is accessed via its corresponding property.

    Attributes:
        name (str): Display name of the user.
        id (int): Numeric user ID.
        image (str): URL of the user's profile image.
        profile_url (str): Full URL to the user's profile page.
        content_count (int | None): Number of content items (posts) the user
            has made. Lazily fetched via profile scrape if not supplied.
        followers (int | None): Number of followers the user has. Lazily
            fetched via profile scrape if not supplied.
        community_reputation (int | None): The user's community reputation
            score. Lazily fetched via profile scrape if not supplied.
        rank (str | None): Display name of the user's rank, as shown in the
            profile header. Lazily fetched via profile scrape if not
            supplied.
        joined (datetime | None): Date and time the user joined. Lazily
            fetched via profile scrape if not supplied.
        last_visited (datetime | None): Date and time of the user's last
            visit. Lazily fetched via profile scrape if not supplied.
        about (About | None): The user's "About" information, including
            detailed rank data and birthday. Lazily fetched via profile
            scrape if not supplied.
        gender (str | None): The user's disclosed gender. Lazily fetched via
            profile scrape if not supplied.
        location (str | None): The user's disclosed location. Lazily fetched
            via profile scrape if not supplied.
        interests (str | None): The user's disclosed interests. Lazily
            fetched via profile scrape if not supplied.

    Note:
        ``content_count``, ``followers``, ``community_reputation``, ``rank``,
        ``joined``, ``last_visited``, ``about``, ``gender``, ``location``,
        and ``interests`` are exposed as read-only properties backed by
        private attributes (e.g. ``_content_count``); see each property's
        own docstring below for details.
    """

    CACHE_MINUTES = 5 * 60

    def __init__(self, session: WebSession, **kwargs: Unpack[WebUserDict]):
        self._session = session
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.image = kwargs.get("image")
        self.profile_url = f"{WebSession.__BASE_URL__}/profile/{self.id}-{self.name.replace(' ', '-')}/"

        self._content_count = kwargs.get("content_count")
        self._followers = kwargs.get("followers")
        self._community_reputation = kwargs.get("community_reputation")
        self._rank = kwargs.get("rank")
        self._joined = kwargs.get("joined")
        self._last_visited = kwargs.get("last_visited")
        self._about = kwargs.get("about")
        self._gender = kwargs.get("gender")
        self._location = kwargs.get("location")
        self._interests = kwargs.get("interests")
        self._contacts = kwargs.get("contacts")

        self._cache_ts = 0

    def _cache_profile(self):
        """Fetch and parse the user's profile page, populating all lazily
        loaded fields.

        Scrapes the profile header (name, rank, image), the profile stats
        block (content count, joined date, last visited date, days won), the
        reputation and follower counts, and the "About"/"Profile
        Information" sections (rank details, birthday, gender, location,
        interests).

        Sets ``self._cached`` to ``True`` once the request has been made, so
        that subsequent property accesses do not trigger another network
        request even if a given field turns out to be unavailable.

        Raises:
            TypeError: If a profile stat is encountered with an unrecognized
                ``data-ui-type`` value.
        """
        current = time.monotonic()

        if current - self._cache_ts < WebUser.CACHE_MINUTES:
            return

        self._cache_ts = current
        response = self._session.request("get", self.profile_url)
        self._cached = True

        soup = BeautifulSoup(response.text, "html.parser")

        profile_header = soup.find("header", {"data-role": "profileHeader"})
        name_container = profile_header.find("div", {"class": "cProfileHeader_name"})

        img_elm = profile_header.find("a", {"class": "ipsUserPhoto"})
        name_elm = name_container.find("h1")
        rank_elm = name_container.find("span")

        self.name = name_elm.text.strip()
        self._rank = rank_elm.text.strip()
        self.image = img_elm.get("href")

        profile_stats = soup.find("div", id="elProfileStats")

        def get_value(name):
            match = profile_stats.find(string=name)
            if not match:
                return None

            info = match.parent.parent
            span = info.find("span", {"data-ui-type": True})

            if not span:
                text = info.text
                return text.replace(name, "").strip()

            ui_type = span.get("data-ui-type")

            if ui_type == "datetime":
                return datetime.fromtimestamp(int(span.get("data-unix")))

            raise TypeError(
                "Unknown ui_type. Please open an issue with this error. If it contains private information please redact it."
                f"{ui_type}: {span}"
            )
            
        self._content_count = get_value("Content Count")
        self._joined = get_value("Joined")
        self._last_visited = get_value("Last visited")
        self._days_won = get_value("Days Won")

        info_column = soup.find("div", id="elProfileInfoColumn")

        community_rep = info_column.find("span", {"class": "cProfileRepScore_points"})
        self._community_reputation = int(community_rep.text)

        follower_container = info_column.find("div", id="elFollowers")
        follower_count = follower_container.find("h2")

        self._followers = int(re.search(r"(\d+)\s+Followers", follower_count.text).group(1))

        def get_group(name):
            match = info_column.find(string=name)
            if not match:
                return None

            return match.parent.parent

        def get_group_elm(group, name):
            match = group.find(string=name)
            if not match:
                return None

            return match.parent.parent.parent

        def get_group_value(group, name):
            elm = get_group_elm(group, name)
            if not elm:
                return None

            return elm.find_all(attrs={"class": "ipsDataItem_generic"})[-1].text.strip()
        
        about = get_group(f"About {self.name}")

        rank_container = get_group_elm(about, "Rank")
        rank_elm = rank_container.find("div")

        rank_name = rank_elm.text.strip()
        rank_level = len(rank_elm.find_all("span", {"class": "ipsPip"}))

        rank = Rank(name=rank_name, level=rank_level)
        birthday = datetime.strptime(get_group_value(about, "Birthday"), "%m/%d/%Y")
        
        self._about = About(rank=rank, birthday=birthday)

        profile_information = get_group("Profile Information")

        self._gender = get_group_value(profile_information, "Gender")
        self._location = get_group_value(profile_information, "Location")
        self._interests = get_group_value(profile_information, "Interests")

        contacts = get_group("Contact Methods")

        self._contacts = Contacts(
                website = get_group_value(contacts, "Website URL"),
                twitter = get_group_value(contacts, "Twitter"),
                mastodon = get_group_value(contacts, "Mastodon"),
                aim = get_group_value(contacts, "AIM"),
                msn = get_group_value(contacts, "MSN"),
                icq = get_group_value(contacts, "ICQ"),
                yahoo = get_group_value(contacts, "Yahoo"),
                xmpp = get_group_value(contacts, "XMPP / Jabber"),
                skype = get_group_value(contacts, "skype"))

    def update(self):
            self._cache_ts = 0
            self._cache_profile()

    @property
    def contacts(self):
        """Contacts | None: The user's contact methods."""
        self._cache_profile()

        return self._contacts

    @property
    def content_count(self):
        """int | None: Number of content items (posts) the user has made."""
        self._cache_profile()

        return self._content_count

    @property
    def followers(self):
        """int | None: Number of followers the user has."""
        self._cache_profile()

        return self._followers

    @property
    def community_reputation(self):
        """int | None: The user's community reputation score. """
        self._cache_profile()

        return self._community_reputation

    @property
    def rank(self):
        """str | None: Display name of the user's rank, as shown in the
        profile header."""
        self._cache_profile()
    
        return self._rank

    @property
    def joined(self):
        """datetime | None: Date and time the user joined. """
        self._cache_profile()
    
        return self._joined

    @property
    def last_visited(self):
        """datetime | None: Date and time of the user's last visit."""
        self._cache_profile()
    
        return self._last_visited

    @property
    def about(self):
        """About | None: The user's "About" information, including detailed
        rank data and birthday."""
        self._cache_profile()
    
        return self._about

    @property
    def gender(self):
        """str | None: The user's disclosed gender."""
        self._cache_profile()
    
        return self._gender

    @property
    def location(self):
        """str | None: The user's disclosed location."""
        self._cache_profile()
    
        return self._location

    @property
    def interests(self):
        """str | None: The user's disclosed interests."""
        self._cache_profile()
    
        return self._interests
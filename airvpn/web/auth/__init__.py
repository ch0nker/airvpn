from __future__ import annotations

from airvpn.web.services import PortManager, APIManager, SessionManager, DeviceManager, DnsManager, InboxManager
from airvpn.web.auth.models import ProfilePrivacy, Notification, Message
from airvpn.web.network import WebSession
from airvpn.exceptions import LoginError
from airvpn.web.user import WebUser

from datetime import datetime
from bs4 import BeautifulSoup
from typing import Optional

import re

class AuthUser(WebUser):
    """Represents the currently logged-in AirVPN user.

    Extends `WebUser` with authentication and account-management
    actions that require an active, authenticated session.

    Attributes:
        session (WebSession): The authenticated web session used for all
            requests made by this user.
        api (APIManager): Manager for the user's api keys.
        ports (PortManager): Manager for the user's forwarded ports.
        devices (DeviceManager): Manager for the user's devices.
        sessions (SessionManager): Manager for the user's active sessions.
        dns (DnsManager): Manager for the user's dns settings.
        premium (bool): Flag for if the user has a current plan.
        name (str): Display name of the user. Inherited from
            `WebUser`.
        id (int): Numeric user ID. Inherited from `WebUser`.
        image (str): URL of the user's profile image. Inherited from
            `WebUser`.
        profile_url (str): Full URL to the user's profile page. Inherited
            from `WebUser`.
        content_count (int | None): Number of content items (posts) the user
            has made. Inherited property from `WebUser`; lazily
            fetched via profile scrape if not already known.
        followers (int | None): Number of followers the user has. Inherited
            property from `WebUser`; lazily fetched via profile
            scrape if not already known.
        community_reputation (int | None): The user's community reputation
            score. Inherited property from `WebUser`; lazily fetched
            via profile scrape if not already known.
        rank (str | None): Display name of the user's rank. Inherited
            property from `WebUser`; lazily fetched via profile
            scrape if not already known.
        joined (datetime | None): Date and time the user joined. Inherited
            property from `WebUser`; lazily fetched via profile
            scrape if not already known.
        last_visited (datetime | None): Date and time of the user's last
            visit. Inherited property from `WebUser`; lazily fetched
            via profile scrape if not already known.
        about (About | None): The user's "About" information. Inherited
            property from `WebUser`; lazily fetched via profile
            scrape if not already known.
        gender (str | None): The user's disclosed gender. Inherited property
            from `WebUser`; lazily fetched via profile scrape if not
            already known.
        location (str | None): The user's disclosed location. Inherited
            property from `WebUser`; lazily fetched via profile
            scrape if not already known.
        interests (str | None): The user's disclosed interests. Inherited
            property from `WebUser`; lazily fetched via profile
            scrape if not already known.
    """
    def __init__(self, username: str, password: str, session: Optional[WebSession] = None):
        self.session = session or WebSession()
        self.premium = False
        self.login(username, password)
        self._ports = None
        self._api = None
        self._sessions = None
        self._devices = None
        self._dns = None
        self._inbox = None

    @property
    def inbox(self):
        """InboxManager: Manger for the user's inbox"""
        if self._inbox is None:
            self._inbox = InboxManager(self.session, self.id)

        return self._inbox

    @property
    def dns(self):
        """DnsManager: Manager for the user's dns settings"""
        if self._dns is None:
            self._dns = DnsManager(self.session)

        return self._dns

    @property
    def api(self):
        """APIManager: Manager for the user's api keys"""
        if self._api is None:
            self._api = APIManager(self.session)

        return self._api

    @property
    def ports(self):
        """PortManager: Manager for the user's forwarded ports."""
        if self._ports is None:
            self._ports = PortManager(self.session)

        return self._ports

    @property
    def sessions(self):
        """SessionManager: Manager for the user's sessions."""
        if self._sessions is None:
            self._sessions = SessionManager(self.session)

        return self._sessions

    @property
    def devices(self):
        """DeviceManager: Manager for the user's devices"""
        if self._devices is None:
            self._devices = DeviceManager(self.session)

        return self._devices

    def follow(self, id: int) -> bool:
        """Follow another member by ID.

        Args:
            id: ID of the member to follow.

        Returns:
            bool: ``True`` if the request succeeded (HTTP 200 or 301), ``False`` otherwise.
        """
        response = self.session.ajax("post", "follow", "notifications", ajax_params = {
            "follow_app": "core",
            "follow_area": "member",
            "follow_id": id
            },
            files=(
                ("follow_submitted", (None, 1)),
                ("csrfKey", (None, self.session.csrf)),
                ("immediate", (None, "follow_type_immediate")),
                ("follow_public", (None, 0)),
                ("follow_public_checkbox", (None, 1))
            ))

        status_code = response.status_code
        return status_code == 200 or status_code == 301

    def edit_profile(self,
                     birthday: datetime = None,
                     website: str = None,
                     twitter: str = None,
                     mastodon: str = None,
                     aim: str = None,
                     msn: str = None,
                     icq: str = None,
                     yahoo: str = None,
                     xmpp: str = None,
                     skype: str = None,
                     gender: str = None,
                     location: str = None,
                     interests: str = None,
                     about_me: str = None,
                     profile_privacy: ProfilePrivacy = None) -> bool:
        """Edit the authenticated user's profile.
 
        Fetches the profile edit form to determine current values and the
        CSRF token, then submits an update to the profile with the given
        fields. Any argument left as ``None`` falls back to the current
        value already on the form or on the user object (and ultimately to
        an empty string, ``ProfilePrivacy.ALL``, or a zeroed-out
        `datetime` for `birthday`), so only the fields the caller wants to
        change need to be supplied.
 
        Args:
            birthday: New birthday to set. Defaults to the user's current
                `about.birthday`, or ``datetime(0, 0, 0)`` if unset.
            website: New personal website URL.
            twitter: New Twitter/X handle or URL.
            mastodon: New Mastodon handle or URL.
            aim: New AIM contact identifier.
            msn: New MSN contact identifier.
            icq: New ICQ contact identifier.
            yahoo: New Yahoo contact identifier.
            xmpp: New XMPP/Jabber contact identifier.
            skype: New Skype contact identifier.
            gender: New disclosed gender.
            location: New disclosed location.
            interests: New disclosed interests.
            about_me: New "About Me" text. Defaults to the current value
                scraped from the edit form's textarea if not provided.
            profile_privacy: New `ProfilePrivacy` setting controlling who
                can view the profile. Defaults to the currently selected
                option on the edit form, or `ProfilePrivacy.ALL` if none
                is selected.
 
        Returns:
            bool: ``True`` if the update request succeeded (HTTP 200 or 301), ``False`` otherwise.
        """

        edit_url = self.profile_url + "edit/"
        response = self.session.session.get(edit_url)

        soup = BeautifulSoup(response.text, "html.parser")
        edit_form = soup.find("form", {"action": edit_url})

        privacy_elm = edit_form.find("select", {"name": "air_ipb_profile_privacy_title"})
        selected_privacy_option = privacy_elm.find("option", {"selected": ""})

        about_me = about_me or edit_form.find("textarea", {"name": "core_pfield_11"}).text
        profile_privacy = profile_privacy or \
            int(selected_privacy_option.get("value")) \
            if selected_privacy_option is not None else \
            ProfilePrivacy.ALL

        birthday = birthday or self.about.birthday or datetime(0,0,0)
        website = website or self.contacts.website or ""
        twitter = twitter or self.contacts.twitter or ""
        mastodon = mastodon or self.contacts.mastodon or ""
        aim = aim or self.contacts.aim or ""
        msn = msn or self.contacts.msn or ""
        icq = icq or self.contacts.icq or ""
        yahoo = yahoo or self.contacts.yahoo or ""
        xmpp = xmpp or self.contacts.xmpp or ""
        skype = skype or self.contacts.skype or ""
        gender = gender or self.gender or ""
        location = location or self.location or ""
        interests = interests or self.interests or ""
        
        response = self.session.session.post(edit_url,
            files=(
                ("form_submitted", (None, 1)),
                ("csrfKey", (None, self.session.csrf)),
                ("bday[month]", (None, birthday.month)),
                ("bday[day]", (None, birthday.day)),
                ("bday[year]", (None, birthday.year)),
                ("core_pfield_3", (None, website)),
                ("core_pfield_12", (None, twitter)),
                ("core_pfield_13", (None, mastodon)),
                ("core_pfield_1", (None, aim)),
                ("core_pfield_2", (None, msn)),
                ("core_pfield_4", (None, icq)),
                ("core_pfield_8", (None, yahoo)),
                ("core_pfield_9", (None, xmpp)),
                ("core_pfield_10", (None, skype)),
                ("core_pfield_5", (None, gender)),
                ("core_pfield_6", (None, location)),
                ("core_pfield_7", (None, interests)),
                ("core_pfield_11", (None, about_me)),
                ("air_ipb_profile_privacy_title", (None, profile_privacy))
            )
        )

        self._about.birthday = birthday
        self._contacts.website = website
        self._contacts.twitter = twitter
        self._contacts.mastodon = mastodon
        self._contacts.aim = aim
        self._contacts.msn = msn
        self._contacts.icq = icq
        self._contacts.yahoo = yahoo
        self._contacts.xmpp = xmpp
        self._contacts.skype = skype
        self._location = location
        self._gender = gender
        self._interests = interests

        return response.status_code == 200 or response.status_code == 301
        
    def unfollow(self, id: int) -> bool:
        """Unfollow a member using their ID.

        Args:
            id: ID of the member to unfollow

        Returns:
            bool: ``True`` if the request succeeded (HTTP 200 or 301), ``False`` otherwise.
        """
        response = self.session.ajax("get", "follow", "notifications", 
                                ajax_params={
                                    "follow_area": "member",
                                    "follow_id": id,
                                    "follow_app": "core"
                                })

        soup = BeautifulSoup(response.text, "html.parser")

        following_member = soup.find("a", {"data-action": "unfollow"})
        if following_member is None:
            return False

        response = self.session.session.get(following_member.get("href"))
        return response.status_code == 200 or response.status_code == 301

    def get_unread_notifications(self) -> tuple[list[Notification], list[Message]]:
        """
        Retrieves a list of unread notifications and messages for the authenticated user.

        Returns:
            tuple[list[Notification], list[Message]]: A tuple containing two lists:
                - A list of `Notification` objects representing unread notifications.
                - A list of `Message` objects representing unread messages.
        """
        data = self.session.ajax("get", "instantNotifications", "ajax", url="", ajax_params={
            "notifications": 0,
            "messages": 0
        }).json()

        notifications = data.get("notifications", {}).get("data", [])
        messages = data.get("messages", {}).get("data", [])

        return (
            [Notification(**notification) for notification in notifications],
            [Message(**message) for message in messages]
        )

    def login(self, username: str, password: str):
        """Log in to the AirVPN website and populate the base user fields.

        Fetches the sign-in form to obtain the CSRF key and reference token,
        submits the login credentials, and on success parses the resulting
        page to extract the authenticated user's ID, name, and profile image,
        as well as the CSRF/anti-cache tokens used for subsequent requests.

        Args:
            username: Account username or email address.
            password: Account password.
            key: The PHPSESSID from your cookies.

        Raises:
            LoginError: If the login request does not redirect away from the
                login page (indicating invalid credentials or a failed
                login attempt).
        """
        response = self.session.request("get", WebSession.__BASE_URL__)

        soup = BeautifulSoup(response.text, "html.parser")

        sign_in_form = soup.find("div", id="elUserSignIn_menu")
        csrf_key_elm = sign_in_form.find("input", { "name": "csrfKey" })
        ref_elm = sign_in_form.find("input", { "name": "ref" })

        csrf_key, ref = csrf_key_elm.get("value"), ref_elm.get("value")

        login_url = f"{WebSession.__BASE_URL__}/login/"

        response = self.session.request("post", login_url, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }, data={
            "csrfKey": csrf_key,
            "ref": ref,
            "auth": username,
            "password": password,
            "remember_me": "1",
            "_processLogin": [ "usernamepassword", "usernamepassword" ]
        })

        if login_url == response.url:
            raise LoginError("Failed to login.")

        soup = BeautifulSoup(response.text, "html.parser")

        self.premium = soup.find("a", {"class": "tooltip-bottom", "data-tooltip": "Your current plan"}) is not None

        user_info = soup.find("li", id="cUserLink")
        profile_url = user_info.find("a", {"class": "ipsUserPhoto"}).get("href")
        name = user_info.find("a", id="elUserLink").text.strip()
        url_info = profile_url.split("profile/")[1].split("-")

        id = int(url_info.pop(0))
        img = user_info.find("img").get("src")

        super().__init__(self.session, name=name, id=id, image=img)
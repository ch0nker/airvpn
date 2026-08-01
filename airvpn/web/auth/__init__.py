from __future__ import annotations

from airvpn.web.network import WebSession
from airvpn.exceptions import LoginError, InvalidPort, APIError
from airvpn.web.auth.models import *
from airvpn.web.user import WebUser
from datetime import datetime
from bs4 import BeautifulSoup

import re
import json
import time

class PortManager:
    """Manages the authenticated user's forwarded ports on AirVPN.

    Wraps the AJAX endpoints behind ``https://airvpn.org/ports/`` to list,
    open, close, and edit forwarded ports, as well as inspect active
    sessions on a port. Any mutating action (`open`, `close`, `edit`)
    triggers a poll loop afterward, since AirVPN applies these changes
    asynchronously on the server side.

    Attributes:
        session (WebSession): The authenticated web session used for all
            requests made by this manager.
        ecsrf (str | None): CSRF token scraped from the ports page, used to
            authorize AJAX requests. Lazily fetched on first use.
        pool (str | None): Identifier of the port pool the user belongs to,
            as reported by the manifest.
        ports (list[Port]): All ports currently owned by the user.
        keys (list[Key]): Keys associated with the user's ports, as reported
            by the manifest.
    """

    __URL__ = "https://airvpn.org/ports/"

    def __init__(self, session: WebSession):
        self.session = session
        self.ecsrf = None
        self.pool = None
        self.ports: list[Port] = []
        self.keys: list[Key] = []
        self._port_map = {}

        self.update()

    def request(self, action: str, **kwargs):
        """Send an AJAX action request to the ports endpoint.

        Automatically attaches the CSRF token (fetching it first if not
        already known) and requests an AJAX-rendered response.

        Args:
            action: Name of the action to perform (e.g. ``"manifest"``,
                ``"insert"``, ``"delete"``, ``"pending"``).
            **kwargs: Additional form fields to send along with the request.

        Returns:
            The parsed JSON response from the server.

        Raises:
            APIError: If the response is a dict containing a non-``None``
                ``"error"`` field.
        """
        self._get_ecsrf()

        data = self.session.session.post(
            PortManager.__URL__,
            data={
                "action": action,
                "ecsrf": self.ecsrf,
                "render": "ajax",
                **kwargs
            }
        ).json()

        if isinstance(data, dict):
            error = data.get("error")
            if error is not None:
                raise APIError(error)

        return data

    def update(self):
        """Refresh the manager's state from the server manifest.

        Fetches the current manifest and repopulates `pool`, `ports`,
        `keys`, and the internal port lookup map from the response.
        """
        self._get_ecsrf()
        manifest = self.request("manifest")
        self.pool = manifest.get("pool")

        self.ports = []
        self._port_map = {}
        for port in manifest.get("ports", []):
            port = Port(**port)
            self._port_map[port.port] = port
            self.ports.append(port)
    
        self.keys = [Key(**key) for key in manifest.get("keys", [])]

    def _get_ecsrf(self):
        if self.ecsrf is not None:
            return

        response = self.session.request("get", PortManager.__URL__)
        soup = BeautifulSoup(response.text, "html.parser")

        data = soup.find("div", id="air_data")
        json_data = json.loads(data.get("data-json"))

        self.ecsrf = json_data.get("ecsrf")

    def poll_update(self):
        """Block until the server finishes applying a pending port change.

        Repeatedly queries the ``"pending"`` action, sleeping one second
        between checks, until the server reports the change is no longer
        pending. Used after actions like `open`, `close`, and `edit` that
        are applied asynchronously.
        """
        while self.request("pending") == "1":
            time.sleep(1)

    def get(self, port: int):
        return self._port_map.get(port)

    def __getitem__(self, port: int) -> None | Port:
        return self.get(port)

    def edit(self, port: int | Port,
             device: str | None = None,
             note: str | None = None,
             protocol: Literal["both", "udp", "tcp"] | None = None,
             localport: int | None = None,
             ddns: str | None = None,
             layer: Literal["both", "v6", "v4"] | None = None):
        """Edit one or more attributes of an existing forwarded port.

        Only fields that are not ``None`` are sent as edit requests. After
        submitting the requested edits, blocks until the server finishes
        applying them.

        Args:
            port: Port number or `Port` instance to edit.
            device: New device name to associate with the port.
            note: New note/description for the port.
            protocol: New protocol restriction (``"both"``, ``"udp"``, or
                ``"tcp"``).
            localport: New local port to forward to.
            ddns: New dynamic DNS hostname for the port.
            layer: New IP layer restriction (``"both"``, ``"v6"``, or
                ``"v4"``).
        """
        port_number = port

        if isinstance(port, Port):
            port_number = port.port
        else:
            port = self[port_number]

        def edit_request(name, value):
            self.request(f"edit_{name}",
                         pool=port.pool,
                         value=value,
                         port=port_number)

        if device is not None:
            edit_request("device", device)
            port.device = device

        if note is not None:
            edit_request("note", note)
            port.notes = note

        if protocol is not None:
            edit_request("protocol", protocol)
            port.protocol = protocol

        if localport is not None:
            edit_request("localport", localport)
            port.local = localport

        if ddns is not None:
            edit_request("ddns", ddns)
            port.dns = ddns

        if layer is not None:
            edit_request("layer", layer)
            port.iplayer = layer

        self.poll_update()

    def open(self, port: int | None = None) -> Port:
        """Open (forward) a new port.

        Args:
            port: Port number to open. Must be ``>= 2048`` and not already
                in use.

        Returns:
            Port: The newly created `Port` instance.

        Raises:
            InvalidPort: If `port` is below 2048, or is already in use.
        """
        if port is not None and port < 2048:
            raise InvalidPort("You can use only ports >=2048, lower ports are already reserved.")

        if self[port] is not None:
            raise InvalidPort(f"The port {port} is already in use.")

        port = port or ""
        data = self.request("insert", port=port)
        self.poll_update()

        result = Port(**data)
        self.ports.append(result)
        self._port_map[result.port] = result

        return result

    def close(self, port: int | Port):
        """Close (delete) an existing forwarded port.

        Args:
            port: Port number or `Port` instance to close.

        Raises:
            InvalidPort: If the given port does not exist.
        """
        pool = self.pool
    
        if isinstance(port, Port):
            pool = port.pool
            port = port.port

        if self.get(port) is None:
            raise InvalidPort(f"Port {port} does not exist.")

        self.request("delete", port=port, pool=pool)
        self.poll_update()

    def get_sessions(self, port: int | Port) -> list[Session]:
        """Retrieve active sessions for a given port.

        Args:
            port: Port number or `Port` instance to query.

        Returns:
            list[Session]: Active sessions currently using the port.
        """
        if isinstance(port, Port):
            port = port.port

        data = self.request("sessions", port=port, pool=self.pool)
        return [Session(session) for session in data.get("items", [])]

    def test_open(self, port: int | Port):
        """Test which of a port's active TCP sessions are reachable.

        Fetches the sessions for `port` and, for each non-UDP session,
        issues a connectivity test against the session's server IP and
        port.

        Args:
            port: Port number or `Port` instance to test.

        Returns:
            list[Session]: The sessions that passed the connectivity test.
        """
        sessions = self.get_sessions(port)
        result = []

        for session in sessions:
            if session.protocol == "udp":
                continue

            data = self.request("test",
                                ip=session.server_ip,
                                port=session.port,
                                pool=session.pool,
                                protocol=session.protocol)

            if data.get("type", "error") == "error":
                continue

            result.append(session)

        return result

class AuthUser(WebUser):
    """Represents the currently logged-in AirVPN user.

    Extends `WebUser` with authentication and account-management
    actions that require an active, authenticated session.

    Attributes:
        session (WebSession): The authenticated web session used for all
            requests made by this user.
        ports (PortManager): Manager for the user's forwarded ports.
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
    def __init__(self, username: str, password: str):
        self.session = WebSession()
        self.login(username, password)
        self._ports = None

    @property
    def ports(self):
        "PortManager: Manager for the user's forwarded ports."
        if self._ports is None:
            self._ports = PortManager(self.session)

        return self._ports

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

    def get_notifications(self):
        """https://airvpn.org/?app=core&module=system&controller=ajax&do=instantNotifications&csrfKey=3c66426ef527c9888e58507320ea156b&notifications=0&messages=0"""
        
    def login(self, username: str, password: str):
        """Log in to the AirVPN website and populate the base user fields.

        Fetches the sign-in form to obtain the CSRF key and reference token,
        submits the login credentials, and on success parses the resulting
        page to extract the authenticated user's ID, name, and profile image,
        as well as the CSRF/anti-cache tokens used for subsequent requests.

        Args:
            username: Account username or email address.
            password: Account password.

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

        user_info = soup.find("li", id="cUserLink").find("a")
        profile_url = user_info.get("href")
        url_info = profile_url.split("profile/")[1].split("-")

        id = int(url_info.pop(0))
        url_info[-1] = url_info[-1][:-1] # strip / from last element
        name = " ".join(url_info)
        img = user_info.find("img").get("src")

        match = re.search(r"csrfKey:\s*\"([0-9a-z]+)\",\s*antiCache:\s*\"([0-9a-z]+)\"", response.text)

        self.session.csrf = match.group(1)
        self.session.anti_cache = match.group(2)

        super().__init__(self.session, name=name, id=id, image=img)
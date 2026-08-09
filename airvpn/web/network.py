from urllib.parse import urlparse, parse_qs, unquote_plus

import requests
import re

__title__ = "Network"

class WebSession:
    """Wraps a `requests.Session` with AirVPN-specific request handling.

    Handles the site's JavaScript-check redirect challenge (computing and
    submitting the required cookie checksum) transparently, and attaches the
    CSRF key to outgoing requests once available.

    Attributes:
        session (requests.Session): Underlying requests session used for all
            HTTP calls.
        csrf (str | None): CSRF key used to authenticate requests, set after
            login.
        anti_cache (str | None): Anti-cache token captured after login.
    """

    __BASE_URL__ = "https://airvpn.org"

    def __init__(self):
        self.session = requests.Session()
        self.csrf = None
        self.anti_cache = None

    def get_checksum(self, token: str) -> int:
        """Compute the checksum required to solve AirVPN's JavaScript-check
        redirect challenge.

        Args:
            token: The raw token extracted from the challenge redirect URL's
                ``aek_id`` query parameter.

        Returns:
            The computed checksum value to be set as the `af3` cookie.
        """
        checksum = 0
        for char in token:
            char_value = ord(char)
            char_value *= char_value * 2 * 3
            char_value *= 5

            checksum = checksum % char_value
            checksum += char_value
            checksum += 23 - 5

        return checksum
    def scrape_csrf(self, response: requests.Response):
        if self.csrf is None:
            match = re.search(r"csrfKey:\s*\"([0-9a-z]+)\",\s*antiCache:\s*\"([0-9a-z]+)\"", response.text)

            self.csrf = match.group(1)
            self.anti_cache = match.group(2)
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Perform an HTTP request, transparently handling AirVPN's
        JavaScript-check redirect challenge if encountered.

        The CSRF key (if set) is automatically added to the request's query
        parameters. If the response indicates the JavaScript-check challenge,
        this method computes the required checksum, sets it as a cookie, and
        retries the request against the redirect target.

        Args:
            method: HTTP method to use (e.g. "get", "post").
            url: URL to request.
            **kwargs: Additional keyword arguments forwarded to
                `requests.Session.request` (e.g. ``data``, ``headers``,
                ``params``).

        Returns:
            requests.Response: The final response, after resolving the JavaScript-check challenge if one was encountered.
        """
        params = kwargs.get("params", {})
        params["csrfKey"] = self.csrf

        response = self.session.request(method, url, **kwargs)
        if "Sorry, AirVPN website require JavaScript." not in response.text:
            self.scrape_csrf(response)
            return response

        redirect_location = response.headers.get("location", response.url)

        parsed = urlparse(redirect_location)
        query_params = parse_qs(parsed.query)

        raw_token = query_params.get("aek_id", [""])[0]
        redirect_path = query_params.get("aek_url", [""])[0]

        token = unquote_plus(raw_token)

        if not redirect_path or not redirect_path.startswith("/"):
            redirect_path = "/"

        if "aek_url" in redirect_path:
            redirect_path = "/"

        checksum = self.get_checksum(token)

        self.session.cookies.set("af3", str(checksum), domain="airvpn.org")

        final_url = f"{WebSession.__BASE_URL__}{redirect_path}"

        response = self.session.request(method, final_url, **kwargs)
        self.scrape_csrf(response)
        return response

    def ajax(self,
            method: str,
            do: str,
            controller: str,
            url = "index.php",
            app = "core",
            module = "system",
            ajax_params: dict = {},
            **kwargs):
        return self.session.request(method, f"{WebSession.__BASE_URL__}/{url}", **kwargs, params={
                    "app": app,
                    "module": module,
                    "controller": controller,
                    "do": do,
                    **ajax_params
                })
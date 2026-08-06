from airvpn.web.network import WebSession
from airvpn.exceptions import APIError
from bs4 import BeautifulSoup

import json
import time

class ClientService:
    """Base class for AJAX-based clients against an AirVPN endpoint.

    Provides shared CSRF-token handling and a generic AJAX request/edit
    interface that endpoint-specific managers (like `PortManager` or
    `APIManager`) can build on.

    Attributes:
        session (WebSession): The authenticated web session used for all
            requests made by this service.
        ecsrf (str | None): CSRF token scraped from the endpoint's page,
            used to authorize AJAX requests. Lazily fetched on first use.
        endpoint (str): URL of the AirVPN page this service issues AJAX
            requests against.
    """
    def __init__(self, endpoint: str, session: WebSession):
        self.session = session
        self.ecsrf = None
        self.endpoint = endpoint

    def _get_ecsrf(self):
            if self.ecsrf is not None:
                return
    
            response = self.session.request("get", self.endpoint)
            soup = BeautifulSoup(response.text, "html.parser")
    
            data = soup.find("div", id="air_data")
            json_data = json.loads(data.get("data-json"))
    
            self.ecsrf = json_data.get("ecsrf")

    def request(self, action: str, **kwargs):
        """Send an AJAX action request to the endpoint.

        Automatically attaches the CSRF token (fetching it first if not
        already known) and requests an AJAX-rendered response.

        Args:
            action: Name of the action to perform.
            **kwargs: Additional form fields to send along with the request.

        Returns:
            The parsed JSON response from the server.

        Raises:
            APIError: If the response is a dict containing a non-``None``
                ``"error"`` field.
        """
        self._get_ecsrf()

        data = self.session.session.post(
            self.endpoint,
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
                if "Invalid CSRF Token" in error:
                    self.ecsrf = None
                    return self.request(action, **kwargs)

                if "Flood protection hit" in error:
                    time.sleep(7)
                    return self.request(action, **kwargs)

                raise APIError(error)

        return data

    def edit_request(self, name, value, **kwargs):
        """Send a generic ``edit_<name>`` action to the endpoint.

        Convenience wrapper around `request` for the common pattern of
        editing a single field by name.

        Args:
            name: Name of the field to edit; sent as the ``edit_{name}``
                action.
            value: New value to set for the field.
            **kwargs: Additional form fields to send along with the request
                (e.g. an ``id`` or ``port`` identifying the target record).

        Returns:
            The parsed JSON response from the server.

        Raises:
            APIError: If the response is a dict containing a non-``None``
                ``"error"`` field.
        """
        return self.request(f"edit_{name}", value=value, **kwargs)
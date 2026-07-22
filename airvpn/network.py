from __future__ import annotations

from airvpn.exceptions import RateLimited, InvalidMethod, InvalidService, APIError
from requests import Session, JSONDecodeError, Response
from typing import Literal
from enum import StrEnum
from math import floor

import warnings
import time

class AirStatus(StrEnum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"

class ServiceType(StrEnum):
    DEVICES = "devices"
    DNS_LISTS = "dns_lists"
    GENERATOR = "generator"
    STATUS = "status"
    USERINFO = "userinfo"
    WHATISMYIP = "whatismyip"
    DISCONNECT = "disconnect"
    NOTIFICATIONS = "notifications"

class AirSession(Session):
    """A `requests.Session` subclass for the AirVPN API with built-in rate limiting.

    Automatically attaches the API key as an `API-KEY` header and enforces
    AirVPN's documented limit of 600 requests per 10 minutes to avoid getting
    IP banned. Requests should be made via `service_request()`, which handles
    endpoint construction, rate limiting, and response/error parsing.

    Attributes:
        BASE_URL: Base URL for all AirVPN API requests.
        REQUESTS_MAX: Maximum requests allowed per `REQUESTS_MAX_MINUTES` window,
            per AirVPN's API documentation.
        REQUESTS_MAX_MINUTES: Length (in minutes) of AirVPN's fixed rate-limit window.
        REQUESTS_PER_MIN: `REQUESTS_MAX` divided evenly across `REQUESTS_MAX_MINUTES`,
            used to scale the limit for a given `rate_window_minutes`.
        rate_window_minutes: The instance's configured window (in minutes) used to
            track and enforce the request rate limit. Clamped to `REQUESTS_MAX_MINUTES`.

    Args:
        api_key: AirVPN API key, sent via the `API-KEY` header.
        rate_window_minutes: Size of the rolling window used for rate limiting.
            Defaults to 5. Values above `REQUESTS_MAX_MINUTES` (10) are clamped,
            with a warning.
    """
    BASE_URL = "https://airvpn.org/api/"

    REQUESTS_MAX = 600
    REQUESTS_MAX_MINUTES = 10
    REQUESTS_PER_MIN = floor(REQUESTS_MAX / REQUESTS_MAX_MINUTES)

    def __init__(self, api_key: str, rate_window_minutes = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers.setdefault("API-KEY", api_key)

        self._rate_window_minutes = 0
        self.rate_window_minutes = rate_window_minutes

        self._request_start = 0
        self._request_counter = 0

    @property
    def rate_window_minutes(self):
        return self._rate_window_minutes

    @rate_window_minutes.setter
    def rate_window_minutes(self, value):
        if value > AirSession.REQUESTS_MAX_MINUTES:
            warnings.warn(f"rate_window_minutes={value} exceeds max of {AirSession.REQUESTS_MAX_MINUTES}; clamping")
            value = AirSession.REQUESTS_MAX_MINUTES

        self._rate_window_minutes = value
    
    def _check_rate_limit(self):
        elapsed = time.monotonic() - self._request_start

        if elapsed > self.rate_window_minutes * 60:
            self._request_counter = 0
            self._request_start = time.monotonic()
            return

        request_limit = self.rate_window_minutes * AirSession.REQUESTS_PER_MIN
        if self._request_counter < request_limit:
            return
        
        raise RateLimited(f"You've hit the {request_limit} requests threshold.")

    def _handle_rate_limit(self):
        if self._request_start == 0:
            self._request_start = time.monotonic()

        self._check_rate_limit()
        self._request_counter += 1

    def _handle_response(self, response: Response) -> dict | bytes:
        try:
            data = response.json()

            error = data.get("error")

            if error is not None:
                raise APIError(error)

            return data
        except JSONDecodeError:
            return response.content

    def service_request(self,
                        method: Literal["get", "post"],
                        service: ServiceType | str,
                        data: dict[str, str] = {},
                        format: Literal["json", "xml", "php", "text"] = "json",
                        **kwargs):
        """Make a rate-limited request to an AirVPN API service.

        Raises:
            InvalidService: if `service` isn't a ServiceType member.
            InvalidMethod: if `method` isn't "get" or "post".
            RateLimited: if the configured request rate limit is hit.
            APIError: if the API responds with an error field.
        """

        try:
            service = ServiceType(service)
        except ValueError:
            raise InvalidService(f"`{service}` is not a valid service. Must be one of: {', '.join(s.value for s in ServiceType)}")

        method = method.lower()
        if method != "get" and method != "post":
            raise InvalidMethod("AirVPN only supports POST and GET requests.")

        url = f"{AirSession.BASE_URL}{service}/"
        params = {"format": format}

        self._handle_rate_limit()

        response = None
        if method == "get":
            params.update(data)
            response = super().get(url, params=params, **kwargs)
        else:
            response = super().post(url, json=data, **kwargs)

        return self._handle_response(response)
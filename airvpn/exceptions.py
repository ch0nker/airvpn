class AirVPNException(Exception):
    """Base exception for all errors raised by the AirVPN API.

    Catch this to handle any AirVPN-related failure without
    distinguishing the cause; prefer the more specific subclasses
    below when you need to branch on what went wrong. This includes
    the exceptions raised directly by the main AirVPN class, as well
    as the `DeviceException` and `GeneratorException` hierarchies
    raised by the Devices manager and config Generator, both of which
    subclass this exception.
    """

class APIKeyRequired(AirVPNException):
    """Raised when a service is accessed without a configured API key.

    Some AirVPN endpoints are user-specific and require an API key to
    be set on the session before use (see services marked
    `__KEY_NEEDED__ = True`). This is raised before any request is
    made, as soon as a call to such a service is attempted without one.
    """

class InvalidService(AirVPNException):
    """Raised when an unrecognized or unsupported service is requested.

    For example, looking up a service by name that doesn't correspond
    to any of AirVPN's known API services/endpoints.
    """

class APIError(AirVPNException):
    """Raised when the service request reports an error"""

class InvalidMethod(AirVPNException):
    """Raised when an invalid method type is requested."""

class RateLimited(AirVPNException):
    """Raised when the rate limit of `rate_window_minutes * AirSession.REQUESTS_PER_MIN` is hit.

    This is based off of the documentation in the FAQ (https://airvpn.org/faq/api/),
    which states you can only make 600 requests every 10 minutes
    or you will be IP banned.
    """

class DeviceException(AirVPNException):
    """Base exception for all errors raised by the Devices manager.

    Subclasses `AirVPNException`. Catch this to handle any
    device-related failure without distinguishing the cause; prefer
    the more specific subclasses below when you need to branch on what
    went wrong, or catch `AirVPNException` to handle any error raised
    by the library as a whole.
    """

class DeviceAPIError(DeviceException):
    """Raised when the AirVPN devices API explicitly reports an error.

    This wraps the `error` message returned in the API's own JSON
    response (e.g. an invalid device ID or invalid action parameters) —
    the request reached the API and was rejected, as opposed to a
    client-side validation or orchestration failure.
    """

class DeviceOperationError(DeviceException):
    """Raised when a multi-step device operation doesn't complete as expected.

    For example, `get(..., create=True)` creating a device but
    receiving no ID back, or a subsequent rename not reporting success.
    The individual API calls didn't necessarily report an `error`, but
    the overall operation couldn't be completed.
    """

class DeviceValidationError(DeviceException):
    """Raised when arguments passed to a Devices method are invalid,
    prior to any request being made.

    For example, calling `modify()` without either a `name` or a
    `description` to change.
    """

class GeneratorException(AirVPNException):
    """Base exception for all errors raised by the config Generator.

    Subclasses `AirVPNException`. Catch this to handle any
    Generator-related failure without distinguishing the cause; prefer
    the more specific subclasses below when you need to branch on what
    went wrong, or catch `AirVPNException` to handle any error raised
    by the library as a whole.
    """

class GeneratorAPIError(GeneratorException):
    """Raised when the AirVPN generator API explicitly reports an error.

    This wraps the `error` message returned in the API's own JSON
    response (e.g. an invalid server name, an invalid device, or a
    permissions issue) — the request reached the API and was rejected,
    as opposed to a client-side parsing or connectivity failure.
    """

class GeneratorResponseError(GeneratorException):
    """Raised when the generator API's response doesn't match the
    expected shape.

    For example, a JSON response that's missing the `options` field
    `create` relies on to build a `ConfigList`. This indicates
    an unexpected/malformed response rather than an error the API
    deliberately reported, and may signal an API change worth
    investigating.
    """


# Exceptions

All errors raised by the AirVPN library inherit from `AirVPNException`, giving you a single root exception to catch when you don't need to distinguish the exact cause. The Devices manager and config Generator also define their own exception subtrees (`DeviceException` and `GeneratorException`), both of which subclass `AirVPNException`.

```py
from airvpn.exceptions import AirVPNException, APIError

try:
    api.devices.get("my-device", create=True)
except APIError as e:
    print(f"AirVPN rejected the request: {e}")
except AirVPNException as e:
    print(f"Something else went wrong: {e}")
```

## Hierarchy

```text
AirVPNException
├── APIKeyRequired
├── InvalidService
├── APIError
├── InvalidMethod
├── RateLimited
├── DeviceException
│   ├── DeviceAPIError
│   ├── DeviceOperationError
│   └── DeviceValidationError
└── GeneratorException
    ├── GeneratorAPIError
    └── GeneratorResponseError
```

## `AirVPNException`

Base exception for all errors raised by the AirVPN library. Catch this to handle any AirVPN-related failure without distinguishing the cause.

| Exception | Raised when |
|---|---|
| `APIKeyRequired` | A service marked `__KEY_NEEDED__ = True` is accessed without a configured API key. Raised before any request is made. |
| `InvalidService` | An unrecognized or unsupported AirVPN service is requested (for example via `get_service`). |
| `APIError` | An AirVPN service request reports an error. |
| `InvalidMethod` | An invalid HTTP method or request method type is requested. |
| `RateLimited` | The library's built-in rate limiter detects that the configured request limit has been exceeded. |

```py
from airvpn import AirVPN
from airvpn.exceptions import APIKeyRequired

api = AirVPN()  # no key provided

try:
    api.devices.list()
except APIKeyRequired:
    print("This service needs an API key.")
```

### Rate limiting example

```py
from airvpn.exceptions import RateLimited

try:
    api.servers.list()
except RateLimited:
    print("Too many requests made in the current rate-limit window.")
```

## `DeviceException`

Base exception for all errors raised by the [Devices](devices.md) manager. Subclasses `AirVPNException`.

| Exception | Raised when |
|---|---|
| `DeviceAPIError` | The AirVPN devices API explicitly reports an error in its JSON response (for example an invalid device ID or invalid action parameters). The request reached the API and was rejected. |
| `DeviceOperationError` | A multi-step device operation doesn't complete as expected even though no individual API call reported an error. For example, `get(..., create=True)` creates a device but no ID is returned, or a rename operation doesn't report success. |
| `DeviceValidationError` | Arguments passed to a Devices method are invalid before any request is made. For example, calling `modify()` without a `name` or `description` to change. |

```py
from airvpn.exceptions import DeviceException

try:
    api.devices.modify(device_id)
except DeviceException as e:
    print(f"Device operation failed: {e}")
```

## `GeneratorException`

Base exception for all errors raised by the config [Generator](generator.md). Subclasses `AirVPNException`.

| Exception | Raised when |
|---|---|
| `GeneratorAPIError` | The AirVPN generator API explicitly reports an error in its JSON response (for example an invalid server name, invalid device, or permissions issue). The request reached the API and was rejected. |
| `GeneratorResponseError` | The generator API's response doesn't match the expected shape. For example, a JSON response missing the `options` field required by `create()`. This indicates an unexpected or malformed response rather than an API-reported error and may signal an API change worth investigating. |

```py
from airvpn.exceptions import GeneratorAPIError, GeneratorResponseError

try:
    config = api.generator.create("Achernar", device="my-device")
except APIError as e:
    print(f"Generator rejected the request: {e}")
except GeneratorResponseError as e:
    print(f"Unexpected response shape: {e}")
```
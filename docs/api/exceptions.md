# Exceptions

All errors raised by the AirVPN library inherit from `AirVPNException`, giving you a single root to catch if you don't need to distinguish the cause. Two submodules — the Devices manager and config Generator — define their own exception subtrees (`DeviceException`, `GeneratorException`) that also subclass `AirVPNException`, so you can catch broadly at the library level or narrowly at the subsystem/cause level.

```py
from airvpn.exceptions import AirVPNException, DeviceAPIError

try:
    api.devices.get("my-device", create=True)
except DeviceAPIError as e:
    print(f"AirVPN rejected the request: {e}")
except AirVPNException as e:
    print(f"Something else went wrong: {e}")
```

## Hierarchy

```
AirVPNException
├── APIKeyRequired
├── InvalidService
├── DeviceException
│   ├── DeviceAPIError
│   ├── DeviceOperationError
│   └── DeviceValidationError
└── GeneratorException
    ├── GeneratorAPIError
    └── GeneratorResponseError
```

## `AirVPNException`

Base exception for all errors raised by the AirVPN API. Catch this to handle any AirVPN-related failure without distinguishing the cause.

| Exception | Raised when |
|---|---|
| `APIKeyRequired` | A service marked `__KEY_NEEDED__ = True` is accessed without a configured API key. Raised before any request is made. |
| `InvalidService` | An unrecognized or unsupported service name is requested (e.g. via `get_service`). |

```py
from airvpn import AirVPN
from airvpn.exceptions import APIKeyRequired

api = AirVPN()  # no key provided

try:
    api.devices.list()
except APIKeyRequired:
    print("This service needs an API key.")
```

## `DeviceException`

Base exception for all errors raised by the [Devices](devices.md) manager. Subclasses `AirVPNException`.

| Exception | Raised when |
|---|---|
| `DeviceAPIError` | The AirVPN devices API explicitly reports an error in its JSON response (e.g. an invalid device ID or invalid action parameters) — the request reached the API and was rejected. |
| `DeviceOperationError` | A multi-step device operation doesn't complete as expected, even though no single API call reported an `error` — e.g. `get(..., create=True)` creates a device but gets no ID back, or a rename doesn't report success. |
| `DeviceValidationError` | Arguments passed to a Devices method are invalid, prior to any request being made — e.g. calling `modify()` without a `name` or `description` to change. |

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
| `GeneratorAPIError` | The AirVPN generator API explicitly reports an error in its JSON response (e.g. an invalid server name, an invalid device, or a permissions issue) — the request reached the API and was rejected. |
| `GeneratorResponseError` | The generator API's response doesn't match the expected shape — e.g. a JSON response missing the `options` field that `create` relies on. Indicates an unexpected/malformed response rather than an API-reported error, and may signal an API change worth investigating. |

```py
from airvpn.exceptions import GeneratorAPIError, GeneratorResponseError

try:
    config = api.generator.create("Achernar", device="my-device")
except GeneratorAPIError as e:
    print(f"Generator rejected the request: {e}")
except GeneratorResponseError as e:
    print(f"Unexpected response shape: {e}")
```
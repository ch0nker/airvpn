# Exceptions

All errors raised by the AirVPN library inherit from `AirVPNException`, giving you a single root exception to catch when you don't need to distinguish the exact cause. The Devices manager, config Generator, and `AirClient` also define their own exception subtrees (`DeviceException`, `GeneratorException`, and `ClientException`), each of which subclasses `AirVPNException`.

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
│   ├── DeviceOperationError
│   └── DeviceValidationError
├── GeneratorException
│   └── GeneratorResponseError
└── ClientException
    ├── RCParseError
    ├── RSAError
    ├── AESEncryptionError
    ├── AESDecryptionError
    └── LoginError
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
| `GeneratorResponseError` | The generator API's response doesn't match the expected shape. For example, a JSON response missing the `options` field required by `create()`. This indicates an unexpected or malformed response rather than an API-reported error and may signal an API change worth investigating. |

```py
from airvpn.exceptions import GeneratorResponseError

try:
    config = api.generator.create("Achernar", device="my-device")
except APIError as e:
    print(f"Generator rejected the request: {e}")
except GeneratorResponseError as e:
    print(f"Unexpected response shape: {e}")
```

## `ClientException`

Base exception for all errors raised by [`AirClient`](client.md), the legacy bootstrap-based (RSA+AES encrypted) protocol client. Subclasses `AirVPNException`. This is a separate protocol from the REST API used by the main `AirVPN` class and its services.

| Exception | Raised when |
|---|---|
| `RCParseError` | A required field (e.g. `rsamodulus`/`rsaexponent`) can't be found in the `.rc` configuration file fetched from `AirClient.RC_URL`. |
| `RSAError` | RSA encryption of the AES key/IV association blob fails. |
| `AESEncryptionError` | AES encryption of the request parameters fails. |
| `AESDecryptionError` | AES decryption or unpadding of a response fails — for example, if the secret key/IV don't match, or the response content is corrupted. |
| `LoginError` | `AirClient.login()`'s response has a `message_action` of `"stop"` — the server rejected the credentials. The exception's message is the server's `message`. |

```py
from airvpn.airclient import AirClient
from airvpn.exceptions import ClientException, RCParseError, LoginError

client = AirClient()

try:
    user = client.login("myusername", "mypassword")
except LoginError as e:
    print(f"Login rejected: {e}")
except RCParseError as e:
    print(f"Couldn't read bootstrap config: {e}")
except ClientException as e:
    print(f"AirClient request failed: {e}")
```
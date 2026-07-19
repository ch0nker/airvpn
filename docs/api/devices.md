# Devices

Manages registered devices/keys associated with the account.

**Access type:** User-specific, API key required.

## Properties

### `devices -> list[Device]`

A cached list of devices registered to the account. On first access it fetches devices from the API; subsequent accesses return the cached list unless a mutating call (`add`, `delete`, `renew`, `modify`) has happened in between, in which case it's refreshed automatically.

```py
for device in api.devices.devices:
    print(device.name, device.status)
```

## Methods

### `list() -> list[Device]`

Lists all devices registered to the account. Always makes a fresh request to the API — use the `devices` property instead if you want caching.

```py
for device in api.devices.list():
    print(device.name, device.status)
```

---

### `get(name: str, create: bool = False) -> Device | None`

Finds a device by name from the device list. If no device with that name exists and `create` is `True`, a new device is registered and renamed to `name`.

```py
device = api.devices.get("My Laptop", create=True)
```

**Raises:**
- `AssertionError` — if `create=True` and creating or renaming the new device fails.

---

### `add() -> str | None`

Registers a new device. Returns the new device's ID, or `None` if not returned by the API.

```py
device_id = api.devices.add()
```

---

### `delete(id: str) -> bool`

Deletes a device by ID. Returns `True` if successful.

```py
api.devices.delete(id="abc123")
```

---

### `renew(id: str) -> bool`

Renews a device by ID. Returns `True` if successful.

```py
api.devices.renew(id="abc123")
```

---

### `modify(id: str, name: str | None = None, description: str | None = None) -> bool`

Modifies a device's name and/or description. At least one of `name` or `description` must be provided.

Returns `True` if successful.

```py
api.devices.modify(id="abc123", name="New Name")
```

**Raises:**
- `AssertionError` — if neither `name` nor `description` is provided.

---

### `action(action: DeviceAction, id=None, name=None, description=None) -> dict`

Low-level method used internally by the methods above to send a raw devices action request. Exposed publicly if you need direct access to the raw response.

**Raises:**
- `AssertionError` — if the API response contains an `error` field.

## Model — `Device`

| Attribute | Type | Description |
|---|---|---|
| `id` | `str` | Unique identifier for the device. |
| `name` | `str` | Display name of the device. |
| `description` | `str` | Description of the device. |
| `version` | `str` | Version of the client/software associated with the device. |
| `renew_first_unix` / `renew_first_date` | `int` / `str` | Timestamp/date of the device's first renewal. |
| `renew_last_unix` / `renew_last_date` | `int` / `str` | Timestamp/date of the device's most recent renewal. |
| `renew_counter` | `int` | Number of times the device has been renewed. |
| `wireguard_public_key` | `str` | The device's WireGuard public key. |
| `wireguard_ipv4` / `wireguard_ipv6` | `str` | IP addresses assigned to the device over WireGuard. |
| `vpn_last_from_unix` / `vpn_last_from_date` | `int` / `str` | Start of the device's last VPN session. |
| `vpn_last_to_unix` / `vpn_last_to_date` | `int` / `str` | End of the device's last VPN session. |
| `vpn_attempt_unix` / `vpn_attempt_date` | `int` / `str` | Timestamp/date of the device's last connection attempt. |
| `vpn_attempt_message` | `str` | Message/result associated with the last connection attempt. |
| `status` | `str` | Current status of the device. |

## Enum — `DeviceAction`

| Value | Description |
|---|---|
| `LIST` | List all devices. |
| `ADD` | Register a new device. |
| `DELETE` | Delete a device. |
| `MODIFY` | Modify a device's name/description. |
| `RENEW` | Renew a device. |
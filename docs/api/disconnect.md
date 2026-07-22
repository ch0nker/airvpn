# disconnect

Requests a disconnection. If none of the filter parameters is specified, disconnects all sessions of the user.

**Access type:** User-specific, API key required.

```py
api.disconnect()                                   # disconnect all sessions
api.disconnect(server="Achernar")                  # disconnect by server name
api.disconnect(device_id="abc123")                 # disconnect by device ID
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `server` | `Server \| str \| None` | Name of the server or the server object to disconnect from. |
| `device_id` | `str \| None` | ID of the device to disconnect. Ignored if `device` is provided. |
| `device` | `Device \| None` | Device to derive the id from to disconnect. Ignored if `device` is provided. |


**Raises:**:
- `APIError` — If the request results in an error.
- `RateLimited` — If too many requests go through.

**Returns:** `int` — the number of sessions that were disconnected.
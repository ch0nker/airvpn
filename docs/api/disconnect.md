# disconnect

Requests a disconnection. If none of the filter parameters is specified, disconnects all sessions of the user.

**Access type:** User-specific, API key required.

```py
api.disconnect()                                   # disconnect all sessions
api.disconnect(server_name="Achernar")              # disconnect by server name
api.disconnect(server=some_server)                  # disconnect by Server object
api.disconnect(device_id="abc123")                  # disconnect by device ID
api.disconnect(device=some_device)                  # disconnect by Device object
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `server` | `Server \| None` | A `Server` object to disconnect from; its `public_name` is used if `server_name` is not explicitly provided. |
| `device` | `Device \| None` | A `Device` object to disconnect; its `id` is used if `device_id` is not explicitly provided. |
| `server_name` | `str \| None` | Name of the server to disconnect from. Ignored if `server` is provided. |
| `device_id` | `str \| None` | ID of the device to disconnect. Ignored if `device` is provided. |

**Returns:** `int` — the number of sessions that were disconnected.
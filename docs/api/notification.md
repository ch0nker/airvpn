# Notification

Send a message to yourself.

Whether the notification appears on the website and/or is sent as an email is controlled in the [notification options](https://airvpn.org/index.php?app=core&module=usercp&tab=core&area=notifications) under **Air → API**.

**Access type:** User-specific, API key required.

## Methods

### `send(subject, body)`

```py
api.notification.send(
    subject="Backup finished",
    body="The nightly backup job completed successfully.",
)
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `subject` | `str` | The notification's subject line. |
| `body` | `str` | The notification's message content. |

**Raises:**:
- `APIError` — If the request results in an error.
- `RateLimited` — If too many requests go through.
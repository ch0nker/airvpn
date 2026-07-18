# send_notification

Send a message to yourself. Useful for scripts or automated processes to notify you of an event that needs attention.

Whether the notification appears on the website and/or is sent as an email is controlled in the [notification options](https://airvpn.org/index.php?app=core&module=usercp&tab=core&area=notifications) under **Air → API**.

**Access type:** User-specific, API key required.

```py
api.send_notification(
    subject="Backup finished",
    body="The nightly backup job completed successfully.",
)
```

## Parameters

| Parameter | Type | Description |
|---|---|---|
| `subject` | `str` | The notification's subject line. |
| `body` | `str` | The notification's message content. |

**Returns:** `bool` — `True` if the notification was sent successfully, `False` otherwise.
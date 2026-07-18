# DnsLists

Fetches available DNS filtering lists.

**Access type:** User-specific, API key required.

```py
lists = api.dns_lists.lists
```

## Attributes

| Attribute | Type | Description |
|---|---|---|
| `lists` | `dict[str, Dns]` | A dict mapping list keys to their corresponding `Dns` objects. |

## Model — `Dns`

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | The DNS list's name. |
| `description` | `str` | Description of the DNS list. |
| `home` | `str \| None` | URL of the DNS list's home page/source, if available. |
| `last_update_unix` | `int` | Unix timestamp of when the DNS list was last updated. |
| `n_items` | `int` | Number of entries in the DNS list. |
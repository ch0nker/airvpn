# UserInfo

Details about yourself, including connection details.

**Access type:** User-specific, API key required.

```py
info = api.userinfo

print(info.user.login)
print(info.connection.server_name)
```

## Attributes

| Attribute | Type | Description |
|---|---|---|
| `user` | `User` | Info about the account that generated the API key. |
| `sessions` | `list[Connection]` | A list of connections ordered oldest to youngest. |
| `connection` | `Connection` | Info about the oldest connection. |
| `result` | `Status` (network status enum) | A status message from network.Status. |

## Model — `User`

| Attribute | Type | Description |
|---|---|---|
| `login` | `str` | The account's login/username. |
| `premium` | `bool` | Whether the account has an active premium subscription. |
| `expiration_days` | `int` | Days remaining until premium expires. |
| `pool` | `int` | Connection pool associated with the account. |
| `posts` | `int` | Total number of posts made by the account. |
| `last_post` | `int` | Unix timestamp of the account's most recent post. |
| `register_unix` / `register_date` | `int` / `str` | Timestamp/date of account registration. |
| `expiration_unix` / `expiration_date` | `int` / `str` | Timestamp/date of premium expiration. |
| `last_visit_unix` / `last_visit_date` | `int` / `str` | Timestamp/date of the account's last site visit. |
| `last_activity_unix` / `last_activity_date` | `int` / `str` | Timestamp/date of the account's last recorded activity. |
| `credits` | `int` | Current credit balance. |
| `last_attempt_unix` / `last_attempt_date` | `int` / `str` | Timestamp/date of the last login attempt. |
| `credit` | `list` | List of credit transaction/history entries. |
| `connected` | `bool` | Whether the account is currently connected/online. |

## Model — `Connection`

| Attribute | Type | Description |
|---|---|---|
| `device_name` / `device_description` | `str` | Name/description of the connected device. |
| `vpn_ip` / `vpn_ipv4` / `vpn_ipv6` | `str` | VPN-assigned IP address(es). |
| `exit_ip` / `exit_ipv4` / `exit_ipv6` | `str` | Exit node IP address(es). |
| `server_name` | `str` | Name of the connected server. |
| `server_country` / `server_country_code` | `str` | Country of the connected server. |
| `server_continent` | `str` | Continent of the connected server. |
| `server_location` | `str` | Specific location/city of the server. |
| `server_bw` | — | Server bandwidth. |
| `bytes_read` / `bytes_write` | `int` | Total bytes received/sent during this connection. |
| `connected_since_date` / `connected_since_unix` | `str` / `int` | When the connection started. |
| `speed_read` / `speed_write` | — | Current/average download/upload speed. |
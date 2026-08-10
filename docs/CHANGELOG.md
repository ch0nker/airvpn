# Changelog

## 0.2.9
- Move `AuthUser.follow` and `AuthUser.unfollow` to `WebUser`.
- Add reading forums via the `ForumManager` class which can be accessed from `AirVPN.web.forums`.
- Add `AirVPN.web.find_member(username: str) -> list[WebUser]` for searching members.
- Remove `AirVPN.client`, instead use `AirVPN.web.user`.

## 0.2.8
- Forgot to test with python 3.11, this fixes it.

## 0.2.7
- Add inbox service to `AuthUser.inbox`

## 0.2.6
- Replace the `AirVPN` class with a wrapper for easier interaction with the other interfaces.
- Add session management through the `SessionManager` class which can be accessed via `AuthUser.sessions`.
- Add devices management through the `DeviceManager` class which can be accesed via `AuthUser.devices`.
- Add dns management through the `DnsManager` class which can be accessed via `AuthUser.dns`
- Add api key management through the `APIManager` class which can be accessed via `AuthUser.api`.
- Add port management through the `PortManager` class which can be accessed via `AuthUser.ports`.
- Add `AuthUser.edit_profile`.
- Add `AuthUser.get_sessions`.
- Add `AuthUser.get_unread_notifications`.
- Add `AuthUser.send_message`.

## 0.2.5
- Read 0.2.0 for the actual changes these past 5 releases has been me shooting myself in the foot.

## 0.2.4
- Forgot to update the version in the script.

## 0.2.3
## 0.2.2
- PyPi issues again

## 0.2.1
- Add some missing fields for pyproject.toml

## 0.2.0
- Use mkdocs for easier documentation.
- Restructured so now the interfaces are split into their own parts.
- Add `WebClient`, for interacting with AirVPN's website. Read more in the [docs](airvpn/web/index.md)

## 0.1.12
- Add `AirClient`, a low-level client for AirVPN's bootstrap api used in AirVPN-Suite's bluetit. Read more in the [docs](airvpn/client/index.md).

## 0.1.11
- For some reason pypi broke with 0.1.10 so this is also 0.1.10

## 0.1.10
- Replace `send_notification` with the service `Notification`
- Removed service specific APIError exceptions `GeneratorAPIError`, and `DeviceAPIError`  

## 0.1.9
- Fix incorrect service name for `send_notification`.
- Add `notification` test

## 0.1.8
- Replace lists in the status service with `StatusList`.
- Removed the `status` attribute from services.
- Replace `AirSession.get` and `AirSession.post` with `AirSession.service_request`.
- Implement rate limiting into `network.AirSession`.
- Renamed `network.Status` to `network.AirStatus`.
- Changed `AirVPN(API_KEY)` to `AirVPN(api_key)` to stick with the naming convention.

## 0.1.7
- Fixed `Devices.modify` always raising an error.
- Add rate limiting to `Devices.delete`.

## 0.1.6
- Rename `create_config` to `create` and `write_config` to `download`.
- Replace assertions with the exceptions `AirVPNException`, `InvalidService`, `DeviceException`, `DeviceAPIError`, `DeviceOperationError`, `DeviceValidationError`, `GeneratorException`, `GeneratorAPIError`, and `GeneratorResponseError`.

## 0.1.5
- Add compatibility for python 3.11

## 0.1.4
- `create_config` now supports multiple files with the `ConfigList` class.
- `write_config` now requests a zip file then extracts all files to the `output_dir` directory.
- Create `Config` and `ConfigList` classes.
- Made it so `__str__` for `Servers` returns the server's public name.
- Changed the `KEY_NEEDED` flag to `__KEY_NEEDED__` for services.
- Moved some imports to be local to cleanup exports for the main file.

## 0.1.3
- Add `write_config` to the generator service.
- Add caching to devices service along with a new way to list devices via `Devices.devices`.
- Add docstring to exception

## 0.1.2
- Remove unused packages
- Add an exception `APIKeyRequired`
- Add options to the arguments `files_binary` and `openvpn_data_ciphers` for `create_config`
- Proper documentation of the argument `download` for `create_config`

## 0.1.1
- Remove `openvpn_allserver` argument from `create_config`

## 0.1.0
- Initial release
- Basic use of AirVPN's API.
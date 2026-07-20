# 0.1.4
- `create_config` now supports multiple files with the `ConfigList` class.
- `write_config` now requests a zip file then extracts all files to the `output_dir` directory.
- Create `Config` and `ConfigList` classes.
- Made it so `__str__` for `Servers` returns the server's public name.
- Changed the `KEY_NEEDED` flag to `__KEY_NEEDED__` for services.
- Moved some imports to be local to cleanup exports for the main file.

# 0.1.3
- Add `write_config` to the generator service.
- Add caching to devices service along with a new way to list devices via `Devices.devices`.
- Add docstring to exception

# 0.1.2
- Remove unused packages
- Add an exception `APIKeyRequired`
- Add options to the arguments `files_binary` and `openvpn_data_ciphers` for `create_config`
- Proper documentation of the argument `download` for `create_config`

# 0.1.1
- Remove `openvpn_allserver` argument from `create_config`

# 0.1.0
- Initial release
- Basic use of AirVPN's API.
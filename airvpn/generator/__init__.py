from __future__ import annotations

from airvpn.exceptions import GeneratorAPIError, GeneratorResponseError
from airvpn.generator.models import *
from airvpn.network import AirSession
from zipfile import ZipFile
from typing import Literal
from io import BytesIO

import os
import json

class Generator:
    """Generates VPN configuration files via the AirVPN config generator API.

    Wraps the same endpoint used by https://airvpn.org/generator, allowing
    programmatic creation of OpenVPN/WireGuard configs for one or more
    servers, systems, and protocols.

    Access type:
        User-specific, API KEY required.
    """

    __KEY_NEEDED__ = True

    def __init__(self, session: AirSession):
        self.session = session

    # If you know how to make it so I don't have to copy and paste
    # these arguments while them staying in the tab-complete let me know in an issue or open a PR please.
    def _create_config(self,
                    servers: str | list[str],
                    device: str,
                    system: SystemType = SystemType.WINDOWS,
                    vpn_type: VpnType = VpnType.WIREGUARD,
                    protocol_type: ProtocolType = ProtocolType.UDP,
                    port: int = 1637,
                    entry_ip: int = 3,
                    download: Literal["auto", "zip", "7z", "tar", "tar.gz", "tar.bz2", "tar.xz"] = "auto",
                    files_binary: Literal["x64", "x32"] = "",
                    files_prefix: str = "",
                    openvpn_directives: str = "",
                    openvpn_data_ciphers: Literal["desktop", "mobile"] = "",
                    openvpn_noembedkeys: bool = None,
                    resolve: bool = False,
                    openvpn_allservers: bool = False,
                    proxy_mode: str = "none",
                    proxy_host: str = "127.0.0.1",
                    proxy_port: str = "8080",
                    proxy_login: str = "",
                    proxy_password: str = "",
                    proxy_auth: str = "none",
                    wireguard_mtu: int = 1320,
                    wireguard_persistent_keepalive: int = 15,
                    iplayer_entry: str = "ipv4",
                    iplayer_exit: str = "both",
                    **kwargs: dict):
            """Build and send a raw config-generator request, returning the raw response body.

            Internal helper shared by `create_config` and `write_config`. Assembles
            the request's query parameters from its arguments (deriving `protocols`
            from `vpn_type`/`entry_ip`/`protocol_type`/`port` and joining `servers`
            into a comma-separated string, unless overridden via `kwargs`), sends
            the request, and validates the response for an API-reported error before
            returning its raw content.

            Args:
                servers: Server name(s) and/or planet grouping(s) to generate
                    configs for. Accepts a single value or a list, which will be
                    comma-joined.
                device: The device profile name to associate with these configs.
                system: Target operating system for the generated configs.
                vpn_type: VPN protocol family (e.g. WireGuard, OpenVPN).
                protocol_type: Transport protocol (UDP or TCP).
                port: Port number to connect on.
                entry_ip: IP version/entry point selector for the connection.
                download: Requested download/archive format for the response.
                files_binary: Optional binary/executable to bundle with the configs.
                files_prefix: Optional filename prefix for generated files.
                openvpn_directives: Additional custom directives to inject into
                    an OpenVPN config.
                openvpn_data_ciphers: Custom data cipher list for OpenVPN.
                openvpn_noembedkeys: Whether to omit embedding keys directly
                    in the OpenVPN config (reference external key files instead).
                resolve: Whether to resolve server hostnames instead of using
                    raw IPs in the config.
                openvpn_allservers: Whether to include all servers in a single
                    OpenVPN config.
                proxy_mode: Proxy mode to configure in the generated config
                    ("none" or a specific proxy type).
                proxy_host: Proxy host address, if proxy_mode is enabled.
                proxy_port: Proxy port, if proxy_mode is enabled.
                proxy_login: Proxy authentication username, if required.
                proxy_password: Proxy authentication password, if required.
                proxy_auth: Proxy authentication method/type, if proxy_mode
                    is enabled.
                wireguard_mtu: MTU value for WireGuard configs.
                wireguard_persistent_keepalive: Persistent keepalive interval,
                    in seconds, for WireGuard configs.
                iplayer_entry: IP layer to use for the entry connection.
                iplayer_exit: IP layer to use for the exit connection.
                **kwargs: Additional/override API parameters, merged in last
                    (taking precedence over derived values like `protocols`
                    and `servers`).

            Raises:
                GeneratorAPIError: If the API response is JSON and reports an
                    `error` field.

            Returns:
                The raw response body (`bytes`) — either a config file, an
                archive, or a JSON payload describing the generated files.
            """
            options = locals()

            options.pop("self")
            options.pop("kwargs")
            options.pop("protocol_type")
            options.pop("vpn_type")
            options.pop("port")
            options.pop("entry_ip")

            if kwargs.get("protocols") is None:
                protocol = f"{vpn_type}_{entry_ip}_{protocol_type}_{port}"
                options["protocols"] = protocol
            if kwargs.get("servers") is None:
                options["servers"] = ",".join(servers) if isinstance(servers, list) else servers

            options = options | kwargs

            response = self.session.get("generator", params=options)

            content = response.content

            if content[:1] == b'{':
                  data = json.loads(content)
                  error = data.get("error")
                  if error is not None:
                      raise GeneratorAPIError(error)

            return content

    def create_config(self,
                    servers: str | list[str],
                    device: str,
                    system: SystemType = SystemType.WINDOWS,
                    vpn_type: VpnType = VpnType.WIREGUARD,
                    protocol_type: ProtocolType = ProtocolType.UDP,
                    port: int = 1637,
                    entry_ip: int = 3,
                    files_binary: Literal["x64", "x32"] = "",
                    files_prefix: str = "",
                    openvpn_directives: str = "",
                    openvpn_data_ciphers: Literal["desktop", "mobile"] = "",
                    openvpn_noembedkeys: bool = None,
                    resolve: bool = False,
                    openvpn_allservers: bool = False,
                    proxy_mode: str = "none",
                    proxy_host: str = "127.0.0.1",
                    proxy_port: str = "8080",
                    proxy_login: str = "",
                    proxy_password: str = "",
                    proxy_auth: str = "none",
                    wireguard_mtu: int = 1320,
                    wireguard_persistent_keepalive: int = 15,
                    iplayer_entry: str = "ipv4",
                    iplayer_exit: str = "both",
                    **kwargs: dict) -> "ConfigList | str":
            """Generate VPN configuration file(s) for one or more servers.
 
            Requests the configuration generator with `download="auto"` and returns the
            generated configuration file(s). When the generator returns a single file
            directly, its contents are returned as a `str`. When the generator instead
            reports a set of files (some configuration options produce multiple files,
            even for a single server), a `ConfigList` is returned — a lazily-fetched,
            sliceable, iterable collection covering those files; individual files aren't
            downloaded until accessed (by index, slice, or iteration), and each fetched
            file is cached afterward.
 
 
            Args:
                servers: Server name(s) and/or planet grouping(s) to generate
                    configs for — e.g. an individual server name, or "earth"
                    for all servers. Accepts a single value or a list, which will
                    be comma-joined; multiple values can be combined with
                    commas (e.g. "earth,SERVERNAME").
                device: The device profile name to associate with these configs.
                system: Target operating system for the generated configs.
                vpn_type: VPN protocol family (e.g. WireGuard, OpenVPN).
                protocol_type: Transport protocol (UDP or TCP).
                port: Port number to connect on.
                entry_ip: IP version/entry point selector for the connection.
                files_binary: Optional binary/executable to bundle with the configs.
                files_prefix: Optional filename prefix for generated files.
                openvpn_directives: Additional custom directives to inject into
                    an OpenVPN config.
                openvpn_data_ciphers: Custom data cipher list for OpenVPN.
                openvpn_noembedkeys: Whether to omit embedding keys directly
                    in the OpenVPN config (reference external key files instead).
                resolve: Whether to resolve server hostnames instead of using
                    raw IPs in the config.
                openvpn_allservers: Whether to include all servers in a single
                    OpenVPN config.
                proxy_mode: Proxy mode to configure in the generated config
                    ("none" or a specific proxy type).
                proxy_host: Proxy host address, if proxy_mode is enabled.
                proxy_port: Proxy port, if proxy_mode is enabled.
                proxy_login: Proxy authentication username, if required.
                proxy_password: Proxy authentication password, if required.
                proxy_auth: Proxy authentication method/type, if proxy_mode
                    is enabled.
                wireguard_mtu: MTU value for WireGuard configs.
                wireguard_persistent_keepalive: Persistent keepalive interval,
                    in seconds, for WireGuard configs.
                iplayer_entry: IP layer to use for the entry connection
                    ("ipv4", "ipv6", or "both").
                iplayer_exit: IP layer to use for the exit connection
                    ("ipv4", "ipv6", or "both").
                **kwargs: Additional API parameters passed through as-is.
                    Used primarily for per-server download selection: pass
                    `server_SERVERNAME="on"` for each server you want included
                    in the downloaded bundle (e.g.
                    `server_earth="on", server_america="on"`). Any other
                    undocumented API parameters can also be passed this way.
 
            Returns:
                A `str` with the config file's contents (Windows-style line
                endings normalized to "\\n") when the generator returns exactly
                one file directly; otherwise a `ConfigList` covering all
                generated files. Fetching an individual `Config` from a
                `ConfigList` decodes it the same way, except any file that
                isn't valid UTF-8 text (e.g. a bundled binary from
                `files_binary`) is returned as a base64 encoded string instead.
            """

            config = self._create_config(servers, device, 
                                system, vpn_type, 
                                protocol_type, port,
                                entry_ip, "auto",
                                files_binary, files_prefix, 
                                openvpn_directives, openvpn_data_ciphers, 
                                openvpn_noembedkeys, resolve, 
                                openvpn_allservers, proxy_mode,
                                proxy_host, proxy_port, 
                                proxy_login, proxy_password, 
                                proxy_auth, wireguard_mtu,
                                wireguard_persistent_keepalive, iplayer_entry,
                                iplayer_exit, **kwargs)
            
            if config[:1] != b"{":
                 return config.decode().replace("\r\n", "\n")
            
            data = json.loads(config)
            files = data.get("files", [])

            option_data = data.get("options")
            if option_data is None:
                raise GeneratorResponseError("Failed to find options")

            option = Options(**option_data)
            if openvpn_noembedkeys is None:
                del option.openvpn_noembedkeys

            return ConfigList(self, option, files)
    
    def write_config(self,
                output_dir: str,
                servers: str | list[str],
                device: str,
                system: SystemType = SystemType.WINDOWS,
                vpn_type: VpnType = VpnType.WIREGUARD,
                protocol_type: ProtocolType = ProtocolType.UDP,
                port: int = 1637,
                entry_ip: int = 3,
                files_binary: Literal["x64", "x32"] = "",
                files_prefix: str = "",
                openvpn_directives: str = "",
                openvpn_data_ciphers: Literal["desktop", "mobile"] = "",
                openvpn_noembedkeys: bool = None,
                resolve: bool = False,
                openvpn_allservers: bool = False,
                proxy_mode: str = "none",
                proxy_host: str = "127.0.0.1",
                proxy_port: str = "8080",
                proxy_login: str = "",
                proxy_password: str = "",
                proxy_auth: str = "none",
                wireguard_mtu: int = 1320,
                wireguard_persistent_keepalive: int = 15,
                iplayer_entry: str = "ipv4",
                iplayer_exit: str = "both",
                **kwargs: dict):
        """Generate VPN configuration file(s) for one or more servers and write them to disk.

        Requests a zip bundle from the generator endpoint (forcing
        `download="zip"` internally) and extracts its contents directly into
        `output_dir`, creating the directory if it doesn't already exist.

        Args:
            output_dir: Directory to extract the generated config files into.
                Created (including parents) if it doesn't already exist.
            servers: Server name(s) and/or planet grouping(s) to generate
                configs for — e.g. an individual server name, or "earth"
                for all servers. Accepts a single value or a list, which will
                be comma-joined; multiple values can be combined with
                commas (e.g. "earth,SERVERNAME"). Note this always
                requests a zip bundle and extracts everything the API
                returns, which may include more than one file even for a
                single server (e.g. SSH configs).
            device: The device profile name to associate with these configs.
            system: Target operating system for the generated configs.
            vpn_type: VPN protocol family (e.g. WireGuard, OpenVPN).
            protocol_type: Transport protocol (UDP or TCP).
            port: Port number to connect on.
            entry_ip: IP version/entry point selector for the connection.
            files_binary: Optional binary/executable to bundle with the configs.
            files_prefix: Optional filename prefix for generated files.
            openvpn_directives: Additional custom directives to inject into
                an OpenVPN config.
            openvpn_data_ciphers: Custom data cipher list for OpenVPN.
            openvpn_noembedkeys: Whether to omit embedding keys directly
                in the OpenVPN config (reference external key files instead).
            resolve: Whether to resolve server hostnames instead of using
                raw IPs in the config.
            openvpn_allservers: Whether to include all servers in a single
                OpenVPN config.
            proxy_mode: Proxy mode to configure in the generated config
                ("none" or a specific proxy type).
            proxy_host: Proxy host address, if proxy_mode is enabled.
            proxy_port: Proxy port, if proxy_mode is enabled.
            proxy_login: Proxy authentication username, if required.
            proxy_password: Proxy authentication password, if required.
            proxy_auth: Proxy authentication method/type, if proxy_mode
                is enabled.
            wireguard_mtu: MTU value for WireGuard configs.
            wireguard_persistent_keepalive: Persistent keepalive interval,
                in seconds, for WireGuard configs.
            iplayer_entry: IP layer to use for the entry connection
                ("ipv4", "ipv6", or "both").
            iplayer_exit: IP layer to use for the exit connection
                ("ipv4", "ipv6", or "both").
            **kwargs: Additional API parameters passed through as-is.
                Used primarily for per-server download selection: pass
                `server_SERVERNAME="on"` for each server you want included
                in the downloaded bundle (e.g.
                `server_earth="on", server_america="on"`). Any other
                undocumented API parameters can also be passed this way.

        Returns:
            None. Files are written directly to `output_dir`.
        """
        zip_bytes = self._create_config(servers, device, 
                                system, vpn_type, 
                                protocol_type, port, 
                                entry_ip, "zip",
                                files_binary, files_prefix, 
                                openvpn_directives, openvpn_data_ciphers, 
                                openvpn_noembedkeys, resolve, 
                                openvpn_allservers, proxy_mode,
                                proxy_host, proxy_port, 
                                proxy_login, proxy_password, 
                                proxy_auth, wireguard_mtu,
                                wireguard_persistent_keepalive, iplayer_entry,
                                iplayer_exit, **kwargs)

        os.makedirs(output_dir, exist_ok=True)

        with ZipFile(BytesIO(zip_bytes)) as zip:
              zip.extractall(output_dir)


class ConfigList:
    """A lazily-fetched, sliceable, iterable collection of generated `Config` files.

    Represents the set of files produced by a single `Generator.create_config`
    call. Individual files are not fetched until accessed (via indexing or
    iteration), and are cached after their first fetch. Slicing returns a
    new, independent `ConfigList` scoped to the sliced subset of files.

    Attributes:
        _index: Cursor used by `__next__` for manual iteration via `next()`.
        _size: Number of files/configs in this list.
        _files: Filenames corresponding to each config, as reported by the
            generator API.
        _generator: The `Generator` instance used to fetch individual files.
        _options: The `Options` used to request each file; `download` is
            mutated per-request to select which file index to fetch.
        _cached_configs: Fetched `Config` objects, indexed in parallel with
            `_files`; unfetched slots are `None`.
    """
    def __init__(self, generator: Generator, options: Options, files: list[str]):
        """Initialize a `ConfigList`.

        Args:
            generator: The `Generator` instance used to fetch individual
                config files on demand.
            options: The `Options` describing the request that produced
                this file set; used as a template for per-file requests.
            files: The filenames of each config in this list, as reported
                by the generator API. The list's length determines the
                size of this `ConfigList`.
        """
        self._index = 0
        self._size = len(files)
        self._files = files
        self._generator = generator
        self._options = options
        self._cached_configs = [None] * self._size

    def __get_config__(self, index: int):
        """Fetch (or return the cached) `Config` at a single integer index.

        Args:
            index: Zero-based index of the file to fetch. Supports
                Python-style negative indexing (e.g. `-1` for the last
                file).

        Raises:
            IndexError: If `index` is out of range (`self._size <= index`).

        Returns:
            The `Config` at `index`, fetching and caching it first if it
            hasn't been fetched yet.
        """
        if self._size <= index:
            raise IndexError
        
        result = self._cached_configs[index]
        if result is not None:
             return result

        self._options.download = str(index) if index >= 0 else str(index + self._size)

        buffer = self._generator._create_config(**self._options.__dict__)
        config = Config(self._files[index], buffer)

        self._cached_configs[index] = config

        return config
    
    def __len__(self):
        """Return the number of configs in this list."""
        return self._size
    
    def __hash__(self):
        """Hash based on this list's `Options`."""
        return hash(self._options)

    def __eq__(self, other):
        """Return whether `other` is a `ConfigList` with an equal hash (i.e. equal `Options`)."""
        return isinstance(other, ConfigList) and hash(self) == hash(other)

    def __getitem__(self, index: int | slice):
        """Fetch a single `Config`, or a new `ConfigList` scoped to a slice.

        Args:
            index: Either an integer index (fetches and returns a single
                `Config`, see `__get_config__`) or a `slice` (returns a
                new, independent `ConfigList` containing only the sliced
                subset of files, cloning `Options` so the original is
                unaffected).

        Returns:
            A `Config` for an integer index, or a new `ConfigList` for a
            slice.
        """
        if isinstance(index, slice):
            start, stop, step = index.indices(self._size)

            result = ConfigList(self._generator, self._options.clone(), self._files[start:stop:step])
            result._cached_configs = self._cached_configs[start:stop:step]
            result._options.servers = self._options.servers[start:stop:step]

            return result

        return self.__get_config__(index)
    
    def __iter__(self):
        """Return a generator yielding each `Config` in this list, in order.

        Each call returns an independent generator with its own position,
        so multiple concurrent or nested iterations over the same
        `ConfigList` don't interfere with each other.
        """
        for i in range(self._size):
            yield self[i]
        
    def __next__(self):
        """Return the next `Config` for manual iteration via `next(config_list)`.

        Uses and advances `self._index` as a persistent cursor, independent
        of `__iter__`'s generator-based iteration.

        Raises:
            StopIteration: Once `self._index` reaches `self._size`.
        """
        if self._index >= self._size:
            raise StopIteration
        
        value = self[self._index]
        self._index += 1

        return value
    
    # TODO: see about appending through either rerunning create_config or
    # seeing if each protocol_type has a specific number of files
    # def append(self, server: str):
    #     self._size += 1
    #     self._cached_configs.append(None)
    #     self._options.servers.append(server)
# WhatIsMyIp

Your IP address, and a check if you are reaching the API from AirVPN's network or not.

**Access type:** Public, no API key required.

```py
info = api.whatismyip

print(info.ip)
print(info.geo_additional.city_name)
```

## Methods

### `get_info() -> IpInfo`

Fetches the current IP address and geolocation info.

## Model — `IpInfo` (`WhatIsMyIp`)

| Attribute | Type | Description |
|---|---|---|
| `ip` | `str` | The detected IP address. |
| `ipv4` / `ipv6` | `bool` | Whether the detected IP is IPv4/IPv6. |
| `airvpn` | `bool` | Whether the detected IP belongs to AirVPN's network. |
| `geo` | `Geo` | Basic geolocation info for the IP. |
| `geo_additional` | `GeoAdditional` | Detailed geolocation and network info. |
| `result` | `Status` (network status enum) | A status message from network.Status. |

## Model — `Geo`

| Attribute | Type | Description |
|---|---|---|
| `code` | `str` | Short code identifying the geographic entity. |
| `name` | `str` | Human-readable name of the geographic entity. |

## Model — `GeoAdditional`

| Attribute | Type | Description |
|---|---|---|
| `ts` | `int` | Unix timestamp of when the geolocation data was generated. |
| `as_number` | `int` | Autonomous System (AS) number associated with the IP. |
| `isp_name` | `str` | Name of the Internet Service Provider. |
| `country_code` / `country_name` | `str` | Country of the IP. |
| `region_code` / `region_name` | `str` | Region/state of the IP. |
| `continent_code` / `continent_name` | `str` | Continent of the IP. |
| `city_name` | `str` | City of the IP. |
| `postal_code` | `str` | Postal/ZIP code. |
| `postal_confidence` | `str` | Confidence level of the postal code accuracy. |
| `latitude` / `longitude` | `float` | Coordinates. |
| `accuracy_radius` | `int` | Estimated accuracy radius, in kilometers. |
| `time_zone` | `str` | Time zone of the location. |
| `metro_code` | `int \| str \| None` | Metro/DMA code, if applicable (typically only present for US-based IPs). |
| `code` / `name` | `str` | Short code / name of the geographic entity. |
| `notes` | `str` | Additional notes about the geolocation data, if any. |
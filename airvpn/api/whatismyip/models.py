from typing import Unpack, TypedDict

class GeoDict(TypedDict, total=False):
    code: str
    name: str

class GeoAdditionalDict(TypedDict, total=False):
    ts: int
    as_number: int
    isp_name: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    continent_code: str
    continent_name: str
    city_name: str
    postal_code: str
    postal_confidence: str
    latitude: float
    longitude: float
    accuracy_radius: int
    time_zone: str
    metro_code: int | str | None
    code: str
    name: str
    notes: str

class IpInfoDict(TypedDict, total=False):
    ip: str
    ipv4: bool
    ipv6: bool
    airvpn: bool
    geo: GeoDict
    geo_additional: GeoAdditionalDict

class Geo:
    """Represents basic geolocation info for an IP address.

    Attributes:
        code: Short code identifying the geographic entity (e.g. country
            or region code).
        name: Human-readable name of the geographic entity.
    """
    def __init__(self, **kwargs: Unpack[GeoDict]):
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")

class GeoAdditional:
    """Represents detailed geolocation and network info for an IP address.

    Attributes:
        ts: Unix timestamp of when the geolocation data was generated.
        as_number: Autonomous System (AS) number associated with the IP.
        isp_name: Name of the Internet Service Provider.
        country_code: ISO country code.
        country_name: Country name.
        region_code: Region/state code.
        region_name: Region/state name.
        continent_code: Continent code.
        continent_name: Continent name.
        city_name: City name.
        postal_code: Postal/ZIP code.
        postal_confidence: Confidence level of the postal code accuracy.
        latitude: Latitude coordinate.
        longitude: Longitude coordinate.
        accuracy_radius: Estimated accuracy radius of the location, in
            kilometers.
        time_zone: Time zone of the location.
        metro_code: Metro/DMA code, if applicable (typically only present
            for US-based IPs); otherwise None.
        code: Short code identifying your country.
        name: Name of your name.
        notes: Additional notes about the geolocation data, if any.
    """
    def __init__(self, **kwargs: Unpack[GeoAdditionalDict]):
        self.ts = kwargs.get("ts")
        self.as_number = kwargs.get("as_number")
        self.isp_name = kwargs.get("isp_name")
        self.country_code = kwargs.get("country_code")
        self.country_name = kwargs.get("country_name")
        self.region_code = kwargs.get("region_code")
        self.region_name = kwargs.get("region_name")
        self.continent_code = kwargs.get("continent_code")
        self.continent_name = kwargs.get("continent_name")
        self.city_name = kwargs.get("city_name")
        self.postal_code = kwargs.get("postal_code")
        self.postal_confidence = kwargs.get("postal_confidence")
        self.latitude = kwargs.get("latitude")
        self.longitude = kwargs.get("longitude")
        self.accuracy_radius = kwargs.get("accuracy_radius")
        self.time_zone = kwargs.get("time_zone")
        self.metro_code = kwargs.get("metro_code")
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")
        self.notes = kwargs.get("notes")

class IpInfo:
    """Represents the response from the whatismyip endpoint.

    Attributes:
        ip: The detected IP address.
        ipv4: Whether the detected IP is an IPv4 address.
        ipv6: Whether the detected IP is an IPv6 address.
        airvpn: Whether the detected IP belongs to AirVPN's network.
        geo: Basic geolocation info for the IP.
        geo_additional: Detailed geolocation and network info for the IP.
    """
    def __init__(self, **kwargs: Unpack[IpInfoDict]):
        self.ip = kwargs.get("ip")
        self.ipv4 = kwargs.get("ipv4")
        self.ipv6 = kwargs.get("ipv6")
        self.airvpn = kwargs.get("airvpn")
        self.geo = Geo(**kwargs.get("geo", {}))
        self.geo_additional = GeoAdditional(**kwargs.get("geo_additional", {}))

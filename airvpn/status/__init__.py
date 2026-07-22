from __future__ import annotations

from airvpn.status.models import Routing, Server, Country, Continent, Planet
from airvpn.network import AirSession
from typing import Type, TypeVar, Iterator, Generic

T = TypeVar("T")

class StatusList(Generic[T]):
    """A lazily-constructed, typed sequence of status model instances.

    Raw API dicts are stored as-is; each item is only converted into a
    `model` instance the first time it's accessed (by index or iteration),
    and the result is cached so repeated access doesn't reconstruct it.

    Args:
        model: The model class to construct each item as (e.g. Server, Country).
        items: Raw dicts from the API response, converted on demand.
    """

    def __init__(self, model: Type[T], items: list[dict]):
        self._model = model
        self._raw = items
        self._cache: dict[int, T] = {}

    def __len__(self):
        return len(self._raw)

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return StatusList(self._model, self._raw[start:stop:step])

        if index < 0:
            index += len(self)

        if index not in self._cache:
            self._cache[index] = self._model(**self._raw[index])

        return self._cache[index]

    def __iter__(self) -> Iterator[T]:
        for i in range(len(self)):
            yield self[i]

class Status:
    """Represents the full VPN network status response.

    Attributes:
        servers: List of individual VPN servers and their current status.
        routing: List of routing nodes and their current status.
        countries: List of aggregate VPN status per country.
        continents: List of aggregate VPN status per continent.
        planets: List of aggregate VPN status globally (typically a single entry).
        deprecated_warning: A deprecated warning from the API.

    Access type:
        Public, no API KEY required.
    """

    __KEY_NEEDED__ = False

    def __init__(self, session: AirSession):
        json = session.service_request("get", "status")

        self.servers = StatusList(Server, json.get("servers", []))
        self.routing = StatusList(Routing, json.get("routing", []))
        self.countries = StatusList(Country, json.get("countries", []))
        self.continents = StatusList(Continent, json.get("continents", []))
        self.planets = StatusList(Planet, json.get("planets", []))

        self.deprecated_warning = json.get("deprecated_warning")
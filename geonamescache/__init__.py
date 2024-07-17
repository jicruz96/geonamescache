# -*- coding: utf-8 -*-
__title__ = 'geonamescache'
__version__ = '2.0.0'
__author__ = 'Ramiro Gómez'
__license__ = 'MIT'


import json
import os
from typing import Any, Dict, List, Mapping, Tuple, TypeVar

from . import geonamesdata
from .types import (
    City,
    Continent,
    Country,
    USCounty,
    USState,
    USStateCode,
    USStateName,
    ContinentCode,
    GeoNameIdStr,
    ISOStr
)

TDict = TypeVar('TDict', bound=Mapping[str, Any])


class GeonamesCache:

    us_states: Dict[USStateCode, USState] = geonamesdata.us_states
    continents: Dict[ContinentCode, Continent] | None = None
    countries: Dict[ISOStr, Country] | None = None
    cities: Dict[GeoNameIdStr, City] | None = None
    cities_items: List[Tuple[GeoNameIdStr, City]] | None = None
    cities_by_names: Dict[str, List[Dict[GeoNameIdStr, City]]] = {}
    us_counties: List[USCounty] | None = None

    def __init__(self, min_city_population: int = 15000):
        self.min_city_population = min_city_population

    def get_dataset_by_key(
        self, dataset: Mapping[str, TDict], key: str
    ) -> Dict[str, TDict]:
        return dict((d[key], d) for c, d in list(dataset.items()))

    def get_continents(self) -> Dict[ContinentCode, Continent]:
        if self.continents is None:
            self.continents = self._load_data(
                self.continents, 'continents.json')
        return self.continents

    def get_countries(self) -> Dict[ISOStr, Country]:
        if self.countries is None:
            self.countries = self._load_data(self.countries, 'countries.json')
        return self.countries

    def get_us_states(self) -> Dict[USStateCode, USState]:
        return self.us_states

    def get_countries_by_names(self) -> Dict[str, Country]:
        return self.get_dataset_by_key(self.get_countries(), 'name')

    def get_us_states_by_names(self) -> Dict[USStateName, USState]:
        return self.get_dataset_by_key(self.get_us_states(), 'name')

    def get_cities(self) -> Dict[GeoNameIdStr, City]:
        """Get a dictionary of cities keyed by geonameid."""

        if self.cities is None:
            self.cities = self._load_data(self.cities, f'cities{self.min_city_population}.json')
        return self.cities

    def get_cities_by_name(self, name: str) -> List[Dict[GeoNameIdStr, City]]:
        """Get a list of city dictionaries with the given name.

        City names cannot be used as keys, as they are not unique.
        """

        if name not in self.cities_by_names:
            if self.cities_items is None:
                self.cities_items = list(self.get_cities().items())
            self.cities_by_names[name] = [dict({gid: city})
                for gid, city in self.cities_items if city['name'] == name]
        return self.cities_by_names[name]

    def get_us_counties(self):
        if self.us_counties is None:
            self.us_counties = self._load_data(self.us_counties, 'us_counties.json')
        return self.us_counties

    def search_cities(
        self,
        query: str,
        attribute: str = 'alternatenames',
        case_sensitive: bool = False,
        contains_search: bool = True,
    ):
        """Search all city records and return list of records, that match query for given attribute."""
        results = []
        query = (case_sensitive and query) or query.casefold()
        for record in self.get_cities().values():
            record_value = record[attribute]
            if contains_search:
                if isinstance(record_value, list):
                    if any(query in ((case_sensitive and value) or value.casefold()) for value in record_value):
                        results.append(record)
                elif query in ((case_sensitive and record_value) or record_value.casefold()):
                    results.append(record)
            else:
                if isinstance(record_value, list):
                    if case_sensitive:
                        if query in record_value:
                            results.append(record)
                    else:
                        if any(query == value.casefold() for value in record_value):
                            results.append(record)
                elif query == ((case_sensitive and record_value) or record_value.casefold()):
                    results.append(record)
        return results

    @staticmethod
    def _load_data(datadict: Dict[str, Any] | None, datafile: str) -> Dict[str, Any]:
        if datadict is None:
            with open(os.path.join(os.path.dirname(__file__), 'data', datafile)) as f:
                datadict = json.load(f)
        return datadict

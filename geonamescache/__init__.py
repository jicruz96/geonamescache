# -*- coding: utf-8 -*-
__title__ = 'geonamescache'
__version__ = '2.0.0'
__author__ = 'Ramiro Gómez'
__license__ = 'MIT'


import functools
import json
import os
from typing import Any, Dict, List, Mapping, Tuple, TypeVar

from . import geonamesdata
from .types import (City, CitySearchAttribute, Continent, ContinentCode,
                    Country, GeoNameIdStr, ISOStr, USCounty, USState,
                    USStateCode, USStateName)

TDict = TypeVar('TDict', bound=Mapping[str, Any])


class GeonamesCache:

    us_states: Dict[USStateCode, USState] = geonamesdata.us_states

    def __init__(self, min_city_population: int = 15000):
        self.min_city_population = min_city_population

    @functools.cached_property
    def continents(self) -> Dict[ContinentCode, Continent]:
        return self._load_data('continents.json')

    @functools.cached_property
    def countries(self) -> Dict[ISOStr, Country]:
        return self._load_data('countries.json')

    @functools.cached_property
    def cities(self) -> Dict[GeoNameIdStr, City]:
        return self._load_data(f'cities{self.min_city_population}.json')

    @functools.cached_property
    def us_counties(self) -> List[USCounty]:
        return self._load_data('us_counties.json')

    @functools.cached_property
    def cities_items(self) -> List[Tuple[GeoNameIdStr, City]]:
        return list(self.cities.items())

    @functools.cached_property
    def cities_by_names(self) -> Dict[str, List[Dict[GeoNameIdStr, City]]]:
        cities_by_names: Dict[str, List[Dict[GeoNameIdStr, City]]] = {}
        for gid, city in self.cities_items:
            if city['name'] not in cities_by_names:
                cities_by_names[city['name']] = []
            cities_by_names[city['name']].append({gid: city})
        return cities_by_names

    def get_dataset_by_key(
        self, dataset: Dict[str, TDict], key: str
    ) -> Dict[str, TDict]:
        return dict((d[key], d) for c, d in list(dataset.items()))

    def get_continents(self) -> Dict[ContinentCode, Continent]:
        return self.continents

    def get_countries(self) -> Dict[ISOStr, Country]:
        return self.countries

    def get_us_states(self) -> Dict[USStateCode, USState]:
        return self.us_states

    def get_countries_by_names(self) -> Dict[str, Country]:
        return self.get_dataset_by_key(self.get_countries(), 'name')

    def get_us_states_by_names(self) -> Dict[USStateName, USState]:
        return self.get_dataset_by_key(self.get_us_states(), 'name')

    def get_cities(self) -> Dict[GeoNameIdStr, City]:
        """Get a dictionary of cities keyed by geonameid."""
        return self.cities

    def get_cities_by_name(self, name: str) -> List[Dict[GeoNameIdStr, City]]:
        """Get a list of city dictionaries with the given name.

        City names cannot be used as keys, as they are not unique.
        """
        return self.cities_by_names.get(name, [])

    def get_us_counties(self):
        return self.us_counties

    def search_cities(
        self,
        query: str,
        attribute: CitySearchAttribute = 'alternatenames',
        case_sensitive: bool = False,
        contains_search: bool = True,
    ) -> List[City]:
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
    def _load_data(datafile: str) -> Any:
        with open(os.path.join(os.path.dirname(__file__), 'data', datafile)) as f:
            return json.load(f)

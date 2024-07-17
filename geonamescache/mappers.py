# -*- coding: utf-8 -*-
from typing import Callable

from geonamescache import GeonamesCache

from . import mappings


def country(
    from_key: str = 'name', to_key: str = 'iso'
) -> Callable[[str], str | int | None]:
    """Creates and returns a mapper function to access country data.

    The mapper function that is returned must be called with one argument. In
    the default case you call it with a name and it returns a 3-letter
    ISO_3166-1 code, e. g. called with ``Spain`` it would return ``ESP``.

    :param from_key: (optional) the country attribute you give as input.
        Defaults to ``name``.
    :param to_key: (optional) the country attribute you want as output.
        Defaults to ``iso``.
    :return: mapper
    :rtype: function
    """

    gc = GeonamesCache()
    dataset = gc.get_dataset_by_key(gc.get_countries(), from_key)

    def mapper(input: str) -> str | int | None:
        # For country name inputs take the names mapping into account.
        if 'name' == from_key:
            input = mappings.country_names.get(input, input)
        # If there is a record return the demanded attribute.
        item = dataset.get(input)
        if item:
            return item[to_key]

    return mapper
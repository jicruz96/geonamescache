import sys
from typing import List, Literal, TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired


class TimeZone(TypedDict):
    gmtOffset: int
    timeZoneId: str
    dstOffset: int


class BBox(TypedDict):
    east: float
    south: float
    north: float
    west: float
    accuracyLevel: int


class _ContinentAlternateNameRequiredKeys(TypedDict):
    name: str
    lang: str


if sys.version_info < (3, 11):

    class ContinentAlternateName(
        _ContinentAlternateNameRequiredKeys, total=False
    ):
        isPreferredName: bool
        isShortName: bool
        isColloquial: bool

else:

    class ContinentAlternateName(_ContinentAlternateNameRequiredKeys):
        isPreferredName: NotRequired[bool]
        isShortName: NotRequired[bool]
        isColloquial: NotRequired[bool]


ContinentCode = Literal['AF', 'AN', 'AS', 'EU', 'NA', 'OC', 'SA']


class _ContinentRequiredKeys(TypedDict):
    lng: str
    geonameId: int
    timezone: TimeZone
    bbox: BBox
    toponymName: str
    asciiName: str
    astergdem: int
    fcl: str
    population: int
    wikipediaURL: str
    adminName5: str
    srtm3: int
    adminName4: str
    adminName3: str
    alternateNames: List[ContinentAlternateName]
    adminName2: str
    name: str
    fclName: str
    fcodeName: str
    adminName1: str
    lat: str
    fcode: str
    continentCode: ContinentCode


if sys.version_info < (3, 11):

    class Continent(_ContinentRequiredKeys, total=False):
        cc2: str

else:

    class Continent(_ContinentRequiredKeys):
        cc2: NotRequired[str]


GeoNameIdStr = str
ISOStr = str


class City(TypedDict):
    geonameid: int
    name: str
    latitude: float
    longitude: float
    countrycode: str
    population: int
    timezone: str
    admin1code: str
    alternatenames: List[str]


class Country(TypedDict):
    geonameid: int
    name: str
    iso: str
    iso3: str
    isonumeric: int
    fips: str
    continentcode: str
    capital: str
    areakm2: int
    population: int
    tld: str
    currencycode: str
    currencyname: str
    phone: str
    postalcoderegex: str
    languages: str
    neighbours: str


USStateCode = Literal[
    'AK',
    'AL',
    'AR',
    'AZ',
    'CA',
    'CO',
    'CT',
    'DC',
    'DE',
    'FL',
    'GA',
    'HI',
    'IA',
    'ID',
    'IL',
    'IN',
    'KS',
    'KY',
    'LA',
    'MA',
    'MD',
    'ME',
    'MI',
    'MN',
    'MO',
    'MS',
    'MT',
    'NC',
    'ND',
    'NE',
    'NH',
    'NJ',
    'NM',
    'NV',
    'NY',
    'OH',
    'OK',
    'OR',
    'PA',
    'RI',
    'SC',
    'SD',
    'TN',
    'TX',
    'UT',
    'VA',
    'VT',
    'WA',
    'WI',
    'WV',
    'WY',
]

USStateName = Literal[
    'Alaska',
    'Alabama',
    'Arkansas',
    'Arizona',
    'California',
    'Colorado',
    'Connecticut',
    'District of Columbia',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Iowa',
    'Idaho',
    'Illinois',
    'Indiana',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Massachusetts',
    'Maryland',
    'Maine',
    'Michigan',
    'Minnesota',
    'Missouri',
    'Mississippi',
    'Montana',
    'North Carolina',
    'North Dakota',
    'Nebraska',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'Nevada',
    'New York',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Virginia',
    'Vermont',
    'Washington',
    'Wisconsin',
    'West Virginia',
    'Wyoming',
]


class USState(TypedDict):
    geonameid: int
    name: USStateName
    code: USStateCode
    fips: str


class USCounty(TypedDict):
    name: str
    fips: str
    state: USStateCode

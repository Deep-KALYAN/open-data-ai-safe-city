# pipeline/__init__.py
# Package pipeline pour SafeCity

from pipeline.fetchers.crimes_fetcher import CrimesFetcher
from pipeline.fetchers.insee_fetcher import INSEEFetcher
from pipeline.fetchers.geo_fetcher import GeoFetcher
from pipeline.storage import (
    save_parquet, 
    load_parquet,
    save_crimes_data,
    save_insee_data,
    save_merged_data,
    load_crimes_data,
    load_insee_data,
    load_merged_data
)

__all__ = [
    "CrimesFetcher",
    "INSEEFetcher",
    "GeoFetcher",
    "save_parquet",
    "load_parquet",
    "save_crimes_data",
    "save_insee_data",
    "save_merged_data",
    "load_crimes_data",
    "load_insee_data",
    "load_merged_data"
]
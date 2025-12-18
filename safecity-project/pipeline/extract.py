import pandas as pd
import geopandas as gpd
from pathlib import Path

RAW_DIR = Path("data/raw")

def load_crimes():
    return pd.read_excel(
        RAW_DIR / "crimes/crimes_gn_2012_2021.xlsx",
        sheet_name=None
    )

def load_population():
    return pd.read_excel(RAW_DIR / "population/insee_population.xlsx")

def load_geo():
    return gpd.read_file(RAW_DIR / "geo/departements.geojson")

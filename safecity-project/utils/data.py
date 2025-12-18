import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/processed")

def load_crime_data():
    return pd.read_parquet(DATA_DIR / "crime_rates.parquet")

def load_geo_data():
    return pd.read_parquet(DATA_DIR / "geo_departements.parquet")

import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def load_population_data(filepath: str) -> pd.DataFrame:
    """
    Load population data from INSEE file
    (CSV or Excel downloaded manually or later automated)
    """
    if filepath.endswith(".xlsx"):
        return pd.read_excel(filepath)
    return pd.read_csv(filepath, sep=";")

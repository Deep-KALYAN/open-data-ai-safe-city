import pandas as pd
import requests
from pathlib import Path

CRIME_DATA_URL = (
    "https://www.data.gouv.fr/api/1/datasets/r/"
    "93438d99-b493-499c-b39f-7de46fa58669"
)

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

CRIME_FILE = RAW_DIR / "crime.csv"


def download_crime_data() -> Path:
    """
    Download crime data using requests (robust SSL handling on Windows)
    """
    if CRIME_FILE.exists():
        return CRIME_FILE

    print("⬇️ Downloading crime data...")

    response = requests.get(CRIME_DATA_URL, timeout=60)
    response.raise_for_status()

    CRIME_FILE.write_bytes(response.content)
    return CRIME_FILE


def load_crime_data() -> pd.DataFrame:
    """
    Load crime dataset as DataFrame
    """
    path = download_crime_data()
    return pd.read_csv(path, sep=";", low_memory=False)


# import pandas as pd
# from pathlib import Path

# CRIME_DATA_URL = (
#     "https://www.data.gouv.fr/api/1/datasets/r/"
#     "93438d99-b493-499c-b39f-7de46fa58669"
# )

# RAW_DIR = Path("data/raw")
# RAW_DIR.mkdir(parents=True, exist_ok=True)


# def download_crime_data() -> Path:
#     """Download raw crime data CSV"""
#     output_path = RAW_DIR / "crime.csv"
#     df = pd.read_csv(CRIME_DATA_URL, sep=";", low_memory=False)
#     df.to_csv(output_path, index=False)
#     return output_path


# def load_crime_data() -> pd.DataFrame:
#     """Load crime dataset as DataFrame"""
#     path = RAW_DIR / "crime.csv"
#     if not path.exists():
#         download_crime_data()
#     return pd.read_csv(path)

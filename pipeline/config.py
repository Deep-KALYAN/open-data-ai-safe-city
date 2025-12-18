# pipeline/config.py
# Configuration centralisee pour SafeCity (avec vraies URLs)

from pathlib import Path
from dataclasses import dataclass

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Creer les dossiers s'ils n'existent pas
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class APIConfig:
    """Configuration pour les APIs."""
    timeout: int = 60
    retries: int = 3
    delay: float = 1.0


# Config pour toutes les sources
CRIMES_API_CONFIG = APIConfig(timeout=60, retries=3, delay=1.0)
INSEE_CONFIG = APIConfig(timeout=60, retries=3, delay=1.0)
GEO_CONFIG = APIConfig(timeout=60, retries=3, delay=1.0)

# URLs des vraies sources
URLS = {
    "crimes": "https://www.data.gouv.fr/api/1/datasets/r/93438d99-b493-499c-b39f-7de46fa58669",
    "insee_population": "https://www.insee.fr/fr/statistiques/8331297",
    "geo_departements": "https://www.data.gouv.fr/api/1/datasets/r/eb36371a-761d-44a8-93ec-3d728bec17ce"
}

# Configuration stockage
PARQUET_CRIMES = PROCESSED_DIR / "crimes_data.parquet"
PARQUET_INSEE = PROCESSED_DIR / "insee_population.parquet"
PARQUET_MERGED = PROCESSED_DIR / "safecity_merged.parquet"
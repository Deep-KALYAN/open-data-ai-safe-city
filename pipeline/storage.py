# pipeline/storage.py
# Fonctions de stockage des donnees en Parquet

import pandas as pd
from pathlib import Path
from pipeline.config import PARQUET_CRIMES, PARQUET_INSEE, PARQUET_MERGED


def save_parquet(df: pd.DataFrame, filepath: Path, compression: str = "snappy") -> None:
    """
    Sauvegarde un DataFrame en Parquet.
    
    Args:
        df: DataFrame a sauvegarder
        filepath: Chemin du fichier Parquet
        compression: Type de compression (snappy, gzip, etc)
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filepath, compression=compression, index=False)
    print(f"✅ Donnees sauvegardees : {filepath.name} ({len(df)} lignes, {df.memory_usage(deep=True).sum() / 1024:.1f} KB)")


def load_parquet(filepath: Path) -> pd.DataFrame:
    """
    Charge un fichier Parquet.
    
    Args:
        filepath: Chemin du fichier Parquet
    
    Returns:
        DataFrame charge
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Fichier non trouve : {filepath}")
    
    df = pd.read_parquet(filepath)
    print(f"✅ Donnees chargees : {filepath.name} ({len(df)} lignes)")
    return df


def save_crimes_data(df: pd.DataFrame) -> None:
    """Sauvegarde les donnees de criminalite."""
    save_parquet(df, PARQUET_CRIMES)


def save_insee_data(df: pd.DataFrame) -> None:
    """Sauvegarde les donnees INSEE."""
    save_parquet(df, PARQUET_INSEE)


def save_merged_data(df: pd.DataFrame) -> None:
    """Sauvegarde les donnees fusionnees."""
    save_parquet(df, PARQUET_MERGED)


def load_crimes_data() -> pd.DataFrame:
    """Charge les donnees de criminalite."""
    return load_parquet(PARQUET_CRIMES)


def load_insee_data() -> pd.DataFrame:
    """Charge les donnees INSEE."""
    return load_parquet(PARQUET_INSEE)


def load_merged_data() -> pd.DataFrame:
    """Charge les donnees fusionnees."""
    return load_parquet(PARQUET_MERGED)


def save_csv(df: pd.DataFrame, filepath: Path) -> None:
    """
    Sauvegarde un DataFrame en CSV (pour debug/export).
    
    Args:
        df: DataFrame a sauvegarder
        filepath: Chemin du fichier CSV
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"✅ CSV sauvegarde : {filepath.name}")


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Retourne un resume des donnees.
    
    Args:
        df: DataFrame a analyser
    
    Returns:
        Dict avec statistiques
    """
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "memory_mb": df.memory_usage(deep=True).sum() / (1024 * 1024)
    }
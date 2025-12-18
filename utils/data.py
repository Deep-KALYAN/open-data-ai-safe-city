# utils/data.py
# Fonctions utilitaires pour charger et transformer les donnees SafeCity

import pandas as pd
import json
from pathlib import Path
from pipeline.config import PARQUET_CRIMES, PARQUET_INSEE, PARQUET_MERGED, RAW_DIR
from pipeline.storage import load_parquet


def load_crimes_data() -> pd.DataFrame:
    """
    Charge les donnees de criminalite depuis Parquet.
    
    Returns:
        DataFrame avec donnees crimes
    """
    try:
        return load_parquet(PARQUET_CRIMES)
    except FileNotFoundError:
        print("❌ Donnees crimes non trouvees. Lancer le pipeline d'abord.")
        return None


def load_insee_data() -> pd.DataFrame:
    """
    Charge les donnees INSEE (population) depuis Parquet.
    
    Returns:
        DataFrame avec donnees population
    """
    try:
        return load_parquet(PARQUET_INSEE)
    except FileNotFoundError:
        print("❌ Donnees INSEE non trouvees. Lancer le pipeline d'abord.")
        return None


def load_merged_data() -> pd.DataFrame:
    """
    Charge les donnees fusionnees (crimes + INSEE) depuis Parquet.
    
    Returns:
        DataFrame avec donnees completes et enrichies
    """
    try:
        return load_parquet(PARQUET_MERGED)
    except FileNotFoundError:
        print("❌ Donnees fusionnees non trouvees. Lancer le pipeline d'abord.")
        return None


def load_geojson() -> dict:
    """
    Charge les contours geographiques depuis GeoJSON.
    
    Returns:
        Dict GeoJSON avec contours departements
    """
    geojson_path = RAW_DIR / "departements_contours.geojson"
    
    if not geojson_path.exists():
        print(f"❌ Fichier GeoJSON non trouve : {geojson_path}")
        return None
    
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    
    print(f"✅ GeoJSON charge : {len(geojson_data.get('features', []))} departements")
    return geojson_data


def get_merged_with_geo() -> tuple:
    """
    Charge les donnees fusionnees avec le GeoJSON.
    
    Returns:
        Tuple (DataFrame merged, Dict GeoJSON)
    """
    merged_df = load_merged_data()
    geojson = load_geojson()
    
    return merged_df, geojson


def get_departments_list() -> list:
    """
    Retourne la liste de tous les departements disponibles.
    
    Returns:
        List de noms departements
    """
    try:
        df = load_merged_data()
        if df is not None and "nom_departement" in df.columns:
            return sorted(df["nom_departement"].unique().tolist())
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
    
    return []


def get_crime_types() -> list:
    """
    Retourne la liste de tous les types de crimes disponibles.
    
    Returns:
        List de types crimes
    """
    try:
        df = load_merged_data()
        if df is not None and "indicateur" in df.columns:
            return sorted(df["indicateur"].unique().tolist())
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
    
    return []


def get_years_available() -> list:
    """
    Retourne la liste de toutes les annees disponibles.
    
    Returns:
        List d'annees
    """
    try:
        df = load_merged_data()
        if df is not None and "annee" in df.columns:
            return sorted(df["annee"].unique().tolist())
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
    
    return []


def filter_by_department(df: pd.DataFrame, department: str) -> pd.DataFrame:
    """
    Filtre les donnees par departement.
    
    Args:
        df: DataFrame source
        department: Nom du departement
    
    Returns:
        DataFrame filtree
    """
    if df is None or "nom_departement" not in df.columns:
        return None
    
    return df[df["nom_departement"] == department]


def filter_by_crime_type(df: pd.DataFrame, crime_type: str) -> pd.DataFrame:
    """
    Filtre les donnees par type de crime.
    
    Args:
        df: DataFrame source
        crime_type: Type de crime
    
    Returns:
        DataFrame filtree
    """
    if df is None or "indicateur" not in df.columns:
        return None
    
    return df[df["indicateur"] == crime_type]


def filter_by_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    Filtre les donnees par annee.
    
    Args:
        df: DataFrame source
        year: Annee
    
    Returns:
        DataFrame filtree
    """
    if df is None or "annee" not in df.columns:
        return None
    
    return df[df["annee"] == year]


def get_top_departments_by_crimes(df: pd.DataFrame, top_n: int = 10, year: int = None) -> pd.DataFrame:
    """
    Retourne les top N departements avec le plus de crimes.
    
    Args:
        df: DataFrame source
        top_n: Nombre de departements a retourner
        year: Annee optionnelle
    
    Returns:
        DataFrame triee
    """
    if df is None:
        return None
    
    data = df.copy()
    
    # Filtrer par annee si specifie
    if year is not None:
        data = data[data["annee"] == year]
    
    # Grouper par departement et sommer les crimes
    top = data.groupby("nom_departement")["nombre"].sum().sort_values(ascending=False).head(top_n)
    
    return top


def get_crime_trend(df: pd.DataFrame, department: str, crime_type: str = None) -> pd.DataFrame:
    """
    Retourne l'evolution temporelle des crimes dans un departement.
    
    Args:
        df: DataFrame source
        department: Nom du departement
        crime_type: Type de crime optionnel
    
    Returns:
        DataFrame avec evolution temporelle
    """
    if df is None:
        return None
    
    data = df.copy()
    
    # Filtrer par departement
    data = data[data["nom_departement"] == department]
    
    # Filtrer par type crime si specifie
    if crime_type is not None:
        data = data[data["indicateur"] == crime_type]
    
    # Trier par annee
    data = data.sort_values("annee")
    
    return data
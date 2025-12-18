# pipeline/run_pipeline.py
# Orchestration du pipeline complet SafeCity

import pandas as pd
from pipeline.fetchers.crimes_fetcher import CrimesFetcher
from pipeline.fetchers.insee_fetcher import INSEEFetcher
from pipeline.fetchers.geo_fetcher import GeoFetcher
from pipeline.storage import save_crimes_data, save_insee_data, save_merged_data


def run_pipeline():
    """
    Execute le pipeline complet d'acquisition et transformation.
    
    Etapes :
    1. Charger donnees crimes
    2. Charger donnees INSEE
    3. Charger donnees geographiques
    4. Nettoyer les donnees
    5. Fusionner crimes + INSEE
    6. Sauvegarder en Parquet
    """
    
    print("="*70)
    print("SAFECITY - PIPELINE D'ACQUISITION DE DONNEES")
    print("="*70 + "\n")
    
    # ETAPE 1 : Charger donnees crimes
    print("ETAPE 1 : Chargement donnees criminalite")
    print("-" * 70)
    crimes_fetcher = CrimesFetcher()
    crimes_df = crimes_fetcher.fetch_from_file()
    
    if crimes_df is None:
        print("❌ Impossible de charger les donnees crimes")
        return
    
    crimes_cleaned = crimes_fetcher.clean_data()
    print(f"Resume crimes : {crimes_fetcher.get_summary()}\n")
    
    # ETAPE 2 : Charger donnees INSEE
    print("ETAPE 2 : Chargement donnees INSEE (population)")
    print("-" * 70)
    insee_fetcher = INSEEFetcher()
    insee_df = insee_fetcher.fetch_from_file()
    
    if insee_df is None:
        print("❌ Impossible de charger les donnees INSEE")
        return
    
    insee_cleaned = insee_fetcher.clean_data()
    print(f"Resume INSEE : {insee_fetcher.get_summary()}\n")
    
    # ETAPE 3 : Charger donnees geographiques
    print("ETAPE 3 : Chargement donnees geographiques")
    print("-" * 70)
    geo_fetcher = GeoFetcher()
    geo_data = geo_fetcher.fetch_from_file()
    
    if geo_data is None:
        print("❌ Impossible de charger les donnees geographiques")
        return
    
    print(f"Resume GEO : {geo_fetcher.get_summary()}\n")
    
    # ETAPE 4 : Fusion donnees
    print("ETAPE 4 : Fusion donnees")
    print("-" * 70)
    
    # Préparer les données pour la fusion
    # Renommer les colonnes si nécessaire
    if "Code_departement" in crimes_cleaned.columns:
        crimes_cleaned = crimes_cleaned.rename(columns={"Code_departement": "departement"})
    
    if "departement" in insee_cleaned.columns and "nom_departement" not in insee_cleaned.columns:
        insee_cleaned["nom_departement"] = insee_cleaned["departement"]
    
    # Fusionner sur (annee, departement)
    merged_df = crimes_cleaned.merge(
        insee_cleaned[["departement", "annee", "population", "nom_departement"]],
        on=["departement", "annee"],
        how="inner"
    )
    
    print(f"✅ Donnees fusionnees : {len(merged_df)} lignes")
    print(f"   Colonnes : {list(merged_df.columns)}\n")
    
    # ETAPE 5 : Stockage
    print("ETAPE 5 : Stockage des donnees")
    print("-" * 70)
    
    save_crimes_data(crimes_cleaned)
    save_insee_data(insee_cleaned)
    save_merged_data(merged_df)
    
    print("\n" + "="*70)
    print("✅ PIPELINE TERMINE AVEC SUCCES !")
    print("="*70)
    
    print(f"\nApercu des donnees fusionnees :")
    print(merged_df.head(15))
    
    print(f"\nStatistiques :")
    print(f"  - Total lignes : {len(merged_df)}")
    print(f"  - Departements : {merged_df['departement'].nunique()}")
    print(f"  - Annees : {sorted(merged_df['annee'].unique().tolist())}")
    print(f"  - Types crimes : {merged_df['indicateur'].nunique()}")
    
    return merged_df


if __name__ == "__main__":
    result = run_pipeline()
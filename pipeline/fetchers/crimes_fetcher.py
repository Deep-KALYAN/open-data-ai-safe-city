# pipeline/fetchers/crimes_fetcher.py
# Fetcher pour les donnees de criminalite (chargement fichier local)

import pandas as pd
from pathlib import Path
from pipeline.config import RAW_DIR


class CrimesFetcher:
    """Fetcher pour charger les donnees de crimes depuis fichier local."""
    
    def __init__(self):
        """Initialise le fetcher."""
        self.data = None
        self.filepath = RAW_DIR / "crimes_data.csv"
    
    def fetch_from_file(self) -> pd.DataFrame:
        """
        Charge les donnees depuis le fichier CSV local.
        
        Returns:
            DataFrame avec donnees crimes
        """
        try:
            print(f"📥 Chargement des donnees de criminalite...")
            print(f"   Fichier : {self.filepath}")
            
            # Charger le CSV avec le bon separateur
            df = pd.read_csv(
                self.filepath,
                sep=";",
                encoding="utf-8"
            )
            
            print(f"✅ Donnees chargees : {len(df)} lignes, {len(df.columns)} colonnes")
            print(f"   Annees : {sorted(df['annee'].unique().tolist())}")
            print(f"   Types crimes : {df['indicateur'].unique().tolist()[:5]}...")
            
            self.data = df
            return df
            
        except Exception as e:
            print(f"❌ Erreur : {str(e)}")
            return None
    
    def clean_data(self) -> pd.DataFrame:
        """
        Nettoie les donnees de criminalite.
        
        Returns:
            DataFrame nettoyees
        """
        if self.data is None:
            print("❌ Pas de donnees a nettoyer")
            return None
        
        print("🧹 Nettoyage des donnees crimes...")
        
        df = self.data.copy()
        
        # Nettoyer les noms de colonnes
        df.columns = (
            df.columns.str.replace('ï»¿', '')
            .str.replace('"', '')
            .str.strip()
        )
        
        # Supprimer les lignes nulles
        initial_rows = len(df)
        df = df.dropna(subset=["Code_departement", "annee", "nombre"])
        
        # Convertir types
        df["Code_departement"] = df["Code_departement"].astype(str).str.strip()
        df["annee"] = df["annee"].astype(int)
        df["nombre"] = df["nombre"].astype(int)
        
        # Virgules → points pour decimaux
        if "taux_pour_mille" in df.columns:
            df["taux_pour_mille"] = (
                df["taux_pour_mille"]
                .astype(str)
                .str.replace(",", ".")
                .astype(float)
            )
        
        print(f"✅ Donnees nettoyees : {initial_rows} → {len(df)} lignes")
        
        return df
    
    def get_data(self) -> pd.DataFrame:
        """Retourne les donnees actuelles."""
        return self.data
    
    def get_summary(self) -> dict:
        """Retourne un resume."""
        if self.data is None:
            return {}
        
        return {
            "total_records": len(self.data),
            "years": sorted(self.data["annee"].unique().tolist()) if "annee" in self.data.columns else [],
            "departments": len(self.data["Code_departement"].unique()) if "Code_departement" in self.data.columns else 0,
            "crime_types": len(self.data["indicateur"].unique()) if "indicateur" in self.data.columns else 0,
            "shape": self.data.shape
        }
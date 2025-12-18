# pipeline/fetchers/insee_fetcher.py
# Fetcher pour les donnees INSEE (chargement fichier local Excel)

import pandas as pd
from pathlib import Path
from pipeline.config import RAW_DIR


class INSEEFetcher:
    """Fetcher pour charger les donnees INSEE depuis fichier Excel local."""
    
    def __init__(self):
        """Initialise le fetcher."""
        self.data = None
        self.filepath = RAW_DIR / "insee_population.xlsx"
    
    def fetch_from_file(self) -> pd.DataFrame:
        """
        Charge les donnees depuis le fichier Excel local.
        
        Returns:
            DataFrame avec donnees population
        """
        try:
            print(f"📥 Chargement des donnees INSEE...")
            print(f"   Fichier : {self.filepath}")
            
            # Lire le fichier Excel
            xls = pd.ExcelFile(self.filepath)
            print(f"✅ Fichier Excel charge : {len(xls.sheet_names)} sheets")
            
            # Charger les sheets recentes (2020-2024)
            dfs = []
            years_to_read = ["2024", "2023", "2022", "2021", "2020"]
            
            for year in years_to_read:
                if year in xls.sheet_names:
                    try:
                        # Charger la sheet (skiprows=4 pour avoir les bonnes colonnes)
                        df_year = pd.read_excel(self.filepath, sheet_name=year, skiprows=4)
                        
                        if not df_year.empty:
                            # Renommer les colonnes
                            df_year.columns = ["departement", "nom_departement"] + list(df_year.columns[2:])
                            
                            # Extraire code dept, nom dept et population totale (colonne 7 = "Total")
                            df_year = df_year[["departement", "nom_departement", "Total"]]
                            df_year = df_year.rename(columns={"Total": "population"})
                            
                            # Ajouter l'annee
                            df_year["annee"] = int(year)
                            
                            # Supprimer les lignes nulles
                            df_year = df_year.dropna()
                            
                            dfs.append(df_year)
                            print(f"   {year} : {len(df_year)} lignes")
                    except Exception as e:
                        print(f"   ⚠️  Erreur lecture {year}: {str(e)}")
            
            if dfs:
                df = pd.concat(dfs, ignore_index=True)
                print(f"✅ Donnees INSEE chargees : {len(df)} lignes")
            else:
                print(f"❌ Aucune donnee trouvee")
                df = None
            
            self.data = df
            return df
            
        except Exception as e:
            print(f"❌ Erreur : {str(e)}")
            return None
    
    def clean_data(self) -> pd.DataFrame:
        """
        Nettoie les donnees INSEE.
        
        Returns:
            DataFrame nettoyees
        """
        if self.data is None:
            print("❌ Pas de donnees a nettoyer")
            return None
        
        print("🧹 Nettoyage des donnees INSEE...")
        
        df = self.data.copy()
        
        # Supprimer les lignes nulles
        initial_rows = len(df)
        df = df.dropna()
        
        # Convertir types
        df["annee"] = df["annee"].astype(int)
        df["population"] = df["population"].astype(int)
        df["departement"] = df["departement"].astype(str).str.strip()
        
        # Filtrer donnees valides
        df = df[df["population"] > 0]
        
        print(f"✅ Donnees INSEE nettoyees : {initial_rows} → {len(df)} lignes")
        
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
            "departments": len(self.data["departement"].unique()) if "departement" in self.data.columns else 0,
            "avg_population": self.data["population"].mean() if "population" in self.data.columns else 0,
            "shape": self.data.shape
        }
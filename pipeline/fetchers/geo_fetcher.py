# pipeline/fetchers/geo_fetcher.py
# Fetcher pour les donnees geographiques (chargement fichier local GeoJSON)

import json
from pathlib import Path
from pipeline.config import RAW_DIR


class GeoFetcher:
    """Fetcher pour charger les donnees geographiques depuis GeoJSON local."""
    
    def __init__(self):
        """Initialise le fetcher."""
        self.data = None
        self.filepath = RAW_DIR / "departements_contours.geojson"
    
    def fetch_from_file(self) -> dict:
        """
        Charge les donnees geographiques depuis le fichier GeoJSON local.
        
        Returns:
            Dict GeoJSON avec contours departements
        """
        try:
            print(f"📥 Chargement des donnees geographiques...")
            print(f"   Fichier : {self.filepath}")
            
            # Charger le GeoJSON
            with open(self.filepath, "r", encoding="utf-8") as f:
                geojson_data = json.load(f)
            
            features = geojson_data.get("features", [])
            print(f"✅ Donnees geographiques chargees !")
            print(f"   Type : {geojson_data.get('type')}")
            print(f"   Nombre de departements : {len(features)}")
            
            if features:
                props = features[0].get("properties", {})
                print(f"   Proprietes : {list(props.keys())}")
            
            self.data = geojson_data
            return geojson_data
            
        except Exception as e:
            print(f"❌ Erreur : {str(e)}")
            return None
    
    def get_data(self) -> dict:
        """Retourne les donnees GeoJSON actuelles."""
        return self.data
    
    def get_summary(self) -> dict:
        """Retourne un resume des donnees."""
        if self.data is None:
            return {}
        
        features = self.data.get("features", [])
        
        # Extraire les codes departement et geometry types en securisant
        departments = []
        geometry_types = []
        
        for f in features:
            # Properties
            props = f.get("properties", {})
            code = props.get("DDEP_C_COD")
            if code:
                departments.append(code)
            
            # Geometry
            geom = f.get("geometry")
            if geom is not None:
                geom_type = geom.get("type")
                if geom_type is not None:
                    geometry_types.append(geom_type)
        
        return {
            "type": self.data.get("type"),
            "total_features": len(features),
            "departments": sorted(departments),
            "geometry_types": list(set(geometry_types))
        }
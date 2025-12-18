# utils/maps.py
# Cartographie Folium pour SafeCity

import folium
from folium import plugins
import pandas as pd
import json
from pathlib import Path


class SafeCityMapper:
    """Creer les cartes interactives pour SafeCity."""
    
    def __init__(self, merged_df: pd.DataFrame, geojson_data: dict):
        """
        Initialise le mapper.
        
        Args:
            merged_df: DataFrame avec donnees crimes + INSEE
            geojson_data: Dict GeoJSON avec contours
        """
        self.data = merged_df
        self.geojson = geojson_data
    
    def create_choropleth_map(self, year: int, crime_type: str = None, center_coords: list = [46.5, 2.5]) -> folium.Map:
        """
        Cree une carte choroplèthe des crimes par departement.
        
        Args:
            year: Annee a afficher
            crime_type: Type de crime (optionnel, tous par defaut)
            center_coords: Coordonnees du centre de la carte
        
        Returns:
            Objet folium.Map
        """
        print(f"🗺️ Creation carte choroplèthe ({year}, {crime_type or 'Tous crimes'})...")
        
        # Filtrer les donnees
        data_filtered = self.data[self.data["annee"] == year].copy()
        
        if crime_type:
            data_filtered = data_filtered[data_filtered["indicateur"] == crime_type]
        
        # Grouper par departement
        data_agg = data_filtered.groupby("departement").agg({
            "nombre": "sum",
            "population": "first"
        }).reset_index()
        
        # Calculer le taux pour 100k habitants
        data_agg["taux_100k"] = (data_agg["nombre"] / data_agg["population"] * 100000).round(2)
        
        # Creer la carte
        m = folium.Map(
            location=center_coords,
            zoom_start=6,
            tiles="OpenStreetMap"
        )
        
        # Ajouter la couche choroplèthe
        try:
            folium.Choropleth(
                geo_data=self.geojson,
                name="Taux crimes",
                data=data_agg,
                columns=["departement", "taux_100k"],
                key_on="feature.properties.DDEP_C_COD",
                fill_color="YlOrRd",
                fill_opacity=0.7,
                line_opacity=0.3,
                legend_name="Taux pour 100k hab"
            ).add_to(m)
        except Exception as e:
            print(f"⚠️ Erreur choroplèthe : {str(e)}")
        
        # Ajouter controle de couches
        folium.LayerControl().add_to(m)
        
        print(f"✅ Carte creee : {len(data_agg)} departements")
        
        return m
    
    def get_summary(self) -> dict:
        """Retourne un resume des capacites de mapping."""
        return {
            "years": sorted(self.data["annee"].unique().tolist()),
            "crime_types": sorted(self.data["indicateur"].unique().tolist()),
            "departments": len(self.data["departement"].unique()),
            "total_records": len(self.data)
        }
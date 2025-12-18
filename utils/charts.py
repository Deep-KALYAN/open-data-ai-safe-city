# utils/charts.py
# Graphiques Plotly pour SafeCity

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class SafeCityCharts:
    """Creer les graphiques interactifs pour SafeCity."""
    
    def __init__(self, merged_df: pd.DataFrame):
        """
        Initialise le charteur.
        
        Args:
            merged_df: DataFrame avec donnees crimes + INSEE
        """
        self.data = merged_df
    
    def create_timeline_chart(self, department: str = None, crime_type: str = None) -> go.Figure:
        """
        Cree un graphique d'evolution temporelle.
        
        Args:
            department: Nom du departement (optionnel)
            crime_type: Type de crime (optionnel)
        
        Returns:
            Figure Plotly
        """
        print(f"📈 Creation graphique evolution temporelle...")
        
        data_filtered = self.data.copy()
        
        if department:
            data_filtered = data_filtered[data_filtered["nom_departement"] == department]
        
        if crime_type:
            data_filtered = data_filtered[data_filtered["indicateur"] == crime_type]
        
        # Grouper par annee
        data_agg = data_filtered.groupby("annee").agg({
            "nombre": "sum"
        }).reset_index()
        
        # Creer le graphique
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data_agg["annee"],
            y=data_agg["nombre"],
            mode="lines+markers",
            name="Nombre crimes",
            line=dict(color="red", width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f"Evolution temporelle des crimes{' - ' + department if department else ''}{' - ' + crime_type if crime_type else ''}",
            xaxis_title="Annee",
            yaxis_title="Nombre crimes",
            hovermode="x unified",
            template="plotly_white"
        )
        
        print(f"✅ Graphique evolution cree")
        
        return fig
    
    def create_bar_chart_top_departments(self, year: int, crime_type: str = None, top_n: int = 10) -> go.Figure:
        """
        Cree un bar chart des top N departements.
        
        Args:
            year: Annee a afficher
            crime_type: Type de crime (optionnel)
            top_n: Nombre de departements a afficher
        
        Returns:
            Figure Plotly
        """
        print(f"📊 Creation bar chart top {top_n} departements...")
        
        data_filtered = self.data[self.data["annee"] == year].copy()
        
        if crime_type:
            data_filtered = data_filtered[data_filtered["indicateur"] == crime_type]
        
        # Grouper par departement
        data_agg = data_filtered.groupby("nom_departement").agg({
            "nombre": "sum"
        }).reset_index()
        
        # Trier et limiter
        data_agg = data_agg.sort_values("nombre", ascending=False).head(top_n)
        
        # Creer le graphique
        fig = px.bar(
            data_agg,
            x="nombre",
            y="nom_departement",
            orientation="h",
            title=f"Top {top_n} departements par criminalite ({year}){' - ' + crime_type if crime_type else ''}",
            labels={"nombre": "Nombre crimes", "nom_departement": "Departement"},
            color="nombre",
            color_continuous_scale="Reds"
        )
        
        fig.update_layout(template="plotly_white", hovermode="y unified")
        
        print(f"✅ Bar chart cree")
        
        return fig
    
    def create_comparison_chart(self, year: int, dept1: str, dept2: str) -> go.Figure:
        """
        Cree un graphique de comparaison entre 2 departements.
        
        Args:
            year: Annee a afficher
            dept1: Nom premier departement
            dept2: Nom second departement
        
        Returns:
            Figure Plotly
        """
        print(f"🔄 Creation graphique comparaison {dept1} vs {dept2}...")
        
        data_filtered = self.data[self.data["annee"] == year].copy()
        
        # Filtrer pour les 2 departements
        dept1_data = data_filtered[data_filtered["nom_departement"] == dept1].groupby("indicateur")["nombre"].sum()
        dept2_data = data_filtered[data_filtered["nom_departement"] == dept2].groupby("indicateur")["nombre"].sum()
        
        # Creer le graphique
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=dept1_data.index,
            y=dept1_data.values,
            name=dept1
        ))
        
        fig.add_trace(go.Bar(
            x=dept2_data.index,
            y=dept2_data.values,
            name=dept2
        ))
        
        fig.update_layout(
            title=f"Comparaison {dept1} vs {dept2} ({year})",
            xaxis_title="Type crime",
            yaxis_title="Nombre crimes",
            barmode="group",
            template="plotly_white",
            hovermode="x unified"
        )
        
        print(f"✅ Graphique comparaison cree")
        
        return fig
    
    def create_pie_chart(self, year: int, department: str = None) -> go.Figure:
        """
        Cree un diagramme circulaire des crimes par type.
        
        Args:
            year: Annee a afficher
            department: Nom du departement (optionnel)
        
        Returns:
            Figure Plotly
        """
        print(f"🥧 Creation pie chart distribution crimes...")
        
        data_filtered = self.data[self.data["annee"] == year].copy()
        
        if department:
            data_filtered = data_filtered[data_filtered["nom_departement"] == department]
        
        # Grouper par type crime
        data_agg = data_filtered.groupby("indicateur")["nombre"].sum().sort_values(ascending=False)
        
        # Creer le graphique
        fig = px.pie(
            values=data_agg.values,
            names=data_agg.index,
            title=f"Distribution des crimes par type ({year}){' - ' + department if department else ''}"
        )
        
        fig.update_layout(template="plotly_white")
        
        print(f"✅ Pie chart cree")
        
        return fig
    
    def get_summary(self) -> dict:
        """Retourne un resume des capacites de charting."""
        return {
            "years": sorted(self.data["annee"].unique().tolist()),
            "crime_types": sorted(self.data["indicateur"].unique().tolist()),
            "departments": sorted(self.data["nom_departement"].unique().tolist())
        }
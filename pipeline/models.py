# pipeline/models.py
# Modeles Pydantic pour validation des donnees SafeCity

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CrimeRecord(BaseModel):
    """Modele pour un enregistrement de crime/delit."""
    
    annee: int = Field(..., description="Annee de l'enregistrement")
    departement: str = Field(..., description="Code departement (75, 69, etc)")
    nom_departement: str = Field(..., description="Nom du departement")
    type_crime: str = Field(..., description="Type de crime/delit")
    nombre: int = Field(..., description="Nombre d'enregistrements")
    taux: Optional[float] = Field(None, description="Taux pour 100k habitants")
    
    class Config:
        json_schema_extra = {
            "example": {
                "annee": 2023,
                "departement": "75",
                "nom_departement": "Paris",
                "type_crime": "Vols",
                "nombre": 15000,
                "taux": 150.5
            }
        }


class PopulationRecord(BaseModel):
    """Modele pour les donnees de population INSEE."""
    
    annee: int = Field(..., description="Annee")
    departement: str = Field(..., description="Code departement")
    nom_departement: str = Field(..., description="Nom du departement")
    population: int = Field(..., description="Population totale")
    densite: float = Field(..., description="Densite (hab/km2)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "annee": 2023,
                "departement": "75",
                "nom_departement": "Paris",
                "population": 2000000,
                "densite": 20000.5
            }
        }


class SafeCityData(BaseModel):
    """Modele pour les donnees fusionnees SafeCity."""
    
    annee: int
    departement: str
    nom_departement: str
    population: int
    densite: float
    type_crime: str
    nombre_crimes: int
    taux_crime: Optional[float] = None
    taux_normalise: Optional[float] = None  # Taux pour 100k hab
    
    class Config:
        json_schema_extra = {
            "example": {
                "annee": 2023,
                "departement": "75",
                "nom_departement": "Paris",
                "population": 2000000,
                "densite": 20000.5,
                "type_crime": "Vols",
                "nombre_crimes": 15000,
                "taux_crime": 750.0,
                "taux_normalise": 150.0
            }
        }


class CrimeTrend(BaseModel):
    """Modele pour une tendance criminelle."""
    
    departement: str
    nom_departement: str
    type_crime: str
    evolution_pct: float = Field(..., description="Pourcentage d'evolution")
    annee_debut: int
    annee_fin: int
    moyenne_taux: float = Field(..., description="Taux moyen periode")
    
    class Config:
        json_schema_extra = {
            "example": {
                "departement": "75",
                "nom_departement": "Paris",
                "type_crime": "Vols",
                "evolution_pct": 12.5,
                "annee_debut": 2020,
                "annee_fin": 2023,
                "moyenne_taux": 145.0
            }
        }


class ComparisonResult(BaseModel):
    """Modele pour une comparaison entre deux departements."""
    
    departement_1: str
    departement_2: str
    type_crime: str
    taux_1: float
    taux_2: float
    difference_pct: float = Field(..., description="Difference en pourcentage")
    plus_securise: str = Field(..., description="Quel dept est plus securise")
    
    class Config:
        json_schema_extra = {
            "example": {
                "departement_1": "75",
                "departement_2": "69",
                "type_crime": "Vols",
                "taux_1": 150.0,
                "taux_2": 100.0,
                "difference_pct": 50.0,
                "plus_securise": "69"
            }
        }
import pandas as pd
from pathlib import Path
from data_ingestion.crime import load_crime_data
from data_processing.crime_categories import CRIME_CATEGORIES

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def add_crime_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a high-level crime_category column based on indicator.
    """
    indicator_to_category = {
        indicator: category
        for category, indicators in CRIME_CATEGORIES.items()
        for indicator in indicators
    }

    df["crime_category"] = df["indicateur"].map(indicator_to_category)
    return df


def build_crime_summary() -> pd.DataFrame:
    """
    Aggregate crime data by department, year, and crime type
    """
    df = load_crime_data()

    # Select relevant columns
    df = df[
        [
            "Code_departement",
            "annee",
            "indicateur",
            "nombre",
            "taux_pour_mille",
            "insee_pop",
        ]
    ]

    # 🔧 FIX FRENCH DECIMAL FORMAT
    df["taux_pour_mille"] = (
        df["taux_pour_mille"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    df["taux_pour_mille"] = pd.to_numeric(
        df["taux_pour_mille"], errors="coerce"
    )

    df["nombre"] = pd.to_numeric(df["nombre"], errors="coerce")
    df["insee_pop"] = pd.to_numeric(df["insee_pop"], errors="coerce")

    # Drop rows with invalid numeric data
    df = df.dropna(subset=["nombre", "taux_pour_mille", "insee_pop"])

    # Aggregate
    summary = (
        df.groupby(["Code_departement", "annee", "indicateur"], as_index=False)
        .agg(
            {
                "nombre": "sum",
                "taux_pour_mille": "mean",
                "insee_pop": "first",
            }
        )
    )

    output_path = PROCESSED_DIR / "crime_summary.csv"
    summary = add_crime_category(summary)
    summary.to_csv(output_path, index=False)

    return summary

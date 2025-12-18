# data_processing/ai_features.py
import pandas as pd


def get_department_ai_features(dept_code: str, year: int):
    df = pd.read_csv("data/processed/department_risk_index.csv")

    row = df[(df["Code_departement"] == dept_code) & (df["annee"] == year)]

    if row.empty:
        return None

    row = row.iloc[0]

    category_breakdown = {
        "Violent": row.get("Violent", 0),
        "Property": row.get("Property", 0),
        "Drugs": row.get("Drugs", 0),
        "Financial": row.get("Financial", 0),
    }

    return {
        "risk_level": row["risk_level"],
        "risk_score": row["risk_score_norm"],
        "category_breakdown": category_breakdown,
        "trend": "Stable compared to previous years.",  # placeholder (we improve later)
    }

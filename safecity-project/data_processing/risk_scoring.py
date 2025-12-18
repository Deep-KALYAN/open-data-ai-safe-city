# data_processing/risk_scoring.py
import pandas as pd
from data_processing.crime_processing import build_crime_summary


def build_department_risk_index(year: int | None = None):
    """
    Build a normalized crime risk index per department and year.
    """

    df = build_crime_summary()

    # Normalize per 1,000 inhabitants
    df["crime_rate_per_1000"] = (df["nombre"] / df["insee_pop"]) * 1000

    # Aggregate by category
    risk = (
        df.groupby(["Code_departement", "annee", "crime_category"])
        .agg(crime_rate_per_1000=("crime_rate_per_1000", "sum"))
        .reset_index()
    )

    # Pivot categories → columns
    risk = risk.pivot_table(
        index=["Code_departement", "annee"],
        columns="crime_category",
        values="crime_rate_per_1000",
        fill_value=0,
    ).reset_index()

    # Composite raw risk score
    risk["risk_score_raw"] = (
        0.4 * risk.get("Violent", 0)
        + 0.3 * risk.get("Property", 0)
        + 0.2 * risk.get("Drugs", 0)
        + 0.1 * risk.get("Financial", 0)
    )

    # Optional year filter
    if year is not None:
        risk = risk[risk["annee"] == year]

    # -----------------------------
    # 🔥 NORMALIZATION (0–100)
    # -----------------------------
    min_score = risk["risk_score_raw"].min()
    max_score = risk["risk_score_raw"].max()

    risk["risk_score_norm"] = (
        (risk["risk_score_raw"] - min_score)
        / (max_score - min_score)
        * 100
    ).round(1)

    # -----------------------------
    # 🚦 RISK LEVELS
    # -----------------------------
    def classify(score):
        if score < 25:
            return "Low"
        elif score < 50:
            return "Medium"
        elif score < 75:
            return "High"
        else:
            return "Critical"

    risk["risk_level"] = risk["risk_score_norm"].apply(classify)

    risk.to_csv(
        "data/processed/department_risk_index.csv",
        index=False,
    )

    return risk


# # data_processing/risk_scoring.py

# import pandas as pd
# from data_processing.crime_processing import build_crime_summary


# def build_department_risk_index(year: int):
#     """
#     Build a normalized crime risk index per department for a given year.
#     """
#     print(f"📊 Building risk index for year {year}...")

#     df = build_crime_summary()

#     df["crime_rate_per_1000"] = (df["nombre"] / df["insee_pop"]) * 1000

#     risk = (
#         df.groupby(["Code_departement", "annee", "crime_category"])
#         .agg(crime_rate_per_1000=("crime_rate_per_1000", "sum"))
#         .reset_index()
#     )

#     risk = (
#         risk.pivot_table(
#             index=["Code_departement", "annee"],
#             columns="crime_category",
#             values="crime_rate_per_1000",
#             fill_value=0,
#         )
#         .reset_index()
#     )

#     risk["risk_score"] = (
#         0.4 * risk.get("Violent", 0)
#         + 0.3 * risk.get("Property", 0)
#         + 0.2 * risk.get("Drugs", 0)
#         + 0.1 * risk.get("Financial", 0)
#     )

#     # Filter to requested year
#     risk = risk[risk["annee"] == year]

#     # One row per department (MANDATORY for maps)
#     risk = (
#         risk.groupby("Code_departement", as_index=False)
#         .agg({"risk_score": "mean"})
#     )

#     print("✅ Risk rows:", len(risk))
#     print("Sample risk data:")
#     print(risk.head())

#     return risk  # 🔥 THIS LINE IS CRITICAL



# import pandas as pd
# from data_processing.crime_processing import build_crime_summary

# def build_department_risk_index(year: int):
#     """
#     Build a normalized crime risk index per department and year.
#     """
#     df = build_crime_summary()

#     # Normalize per 1,000 inhabitants
#     df["crime_rate_per_1000"] = (df["nombre"] / df["insee_pop"]) * 1000

#     # Aggregate by category
#     # risk = (
#     #     df.groupby(["Code_departement", "annee", "crime_category"])
#     #     .agg(
#     #         crime_rate_per_1000=("crime_rate_per_1000", "sum"),
#     #     )
#     #     .reset_index()
#     # )
#     risk = (
#         risk.groupby("Code_departement", as_index=False)
#         .agg({"risk_score": "mean"})
#     )

#     # Pivot categories → columns
#     risk = risk.pivot_table(
#         index=["Code_departement", "annee"],
#         columns="crime_category",
#         values="crime_rate_per_1000",
#         fill_value=0,
#     ).reset_index()

#     # Composite risk score (simple weighted sum)
#     risk["risk_score"] = (
#         0.4 * risk.get("Violent", 0)
#         + 0.3 * risk.get("Property", 0)
#         + 0.2 * risk.get("Drugs", 0)
#         + 0.1 * risk.get("Financial", 0)
#     )

#     risk = risk[risk["annee"] == year]

#     risk.to_csv("data/processed/department_risk_index.csv", index=False)
#     return risk

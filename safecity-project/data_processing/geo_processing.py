# data_processing/geo_processing.py

import geopandas as gpd
from data_processing.risk_scoring import build_department_risk_index


def build_geo_risk(year: int):
    geo = gpd.read_file("data/raw/geo/departements.geojson")

    geo["Code_departement"] = geo["DDEP_C_COD"].astype(str).str.zfill(2)

    print("GEO COLUMNS:", list(geo.columns))
    print("Geo department codes (sample):", geo["Code_departement"].unique()[:10])

    risk = build_department_risk_index(year)

    # 🛑 HARD FAIL IF SOMETHING IS WRONG
    if risk is None:
        raise RuntimeError("❌ build_department_risk_index returned None")

    print("\nRISK COLUMNS:", list(risk.columns))
    print("Risk department codes (sample):", risk["Code_departement"].unique()[:10])

    gdf = geo.merge(risk, on="Code_departement", how="left")

    print("\nAFTER MERGE:")
    print(
        gdf[
            [
                "Code_departement",
                "risk_score_norm",
                "risk_level",
            ]
        ].head()
    )
    print("Rows:", len(gdf))
    print(
        "Missing risk_score_norm:",
        gdf["risk_score_norm"].isna().sum()
    )

    return gdf


# # import geopandas as gpd
# # from data_processing.risk_scoring import build_department_risk_index

# def build_geo_risk(year: int):
#     import geopandas as gpd
#     from data_processing.risk_scoring import build_department_risk_index

#     # Load geo data
#     geo = gpd.read_file("data/raw/geo/departements.geojson")

#     print("GEO COLUMNS:", list(geo.columns))
#     print("FIRST GEO ROW:")
#     print(geo.head(1))

#     # IMPORTANT: correct department code
#     geo["Code_departement"] = geo["DDEP_C_COD"].astype(str).str.zfill(2)

#     print("\nGeo department codes (sample):")
#     print(geo["Code_departement"].head(10).tolist())

#     # Load risk data
#     risk = build_department_risk_index(year)

#     print("\nRISK COLUMNS:", list(risk.columns))
#     print("FIRST RISK ROWS:")
#     print(risk.head())

#     print("\nRisk department codes (sample):")
#     print(risk["Code_departement"].head(10).tolist())

#     # Merge
#     gdf = geo.merge(risk, on="Code_departement", how="left")

#     print("\nAFTER MERGE:")
#     print(gdf[["Code_departement", "risk_score"]].head(10))
#     print("Missing risk_score:", gdf["risk_score"].isna().sum())
#     print("ROWS AFTER MERGE:", len(gdf))
#     print("UNIQUE DEPARTMENTS:", gdf["Code_departement"].nunique())
#     return gdf



# import geopandas as gpd
# from data_processing.risk_scoring import build_department_risk_index


# def build_geo_risk(year: int):
#     # Load geo data
#     geo = gpd.read_file("data/raw/geo/departements.geojson")

#     # ✅ INSEE department code column
#     geo["Code_departement"] = (
#         geo["DDEP_C_COD"].astype(str).str.zfill(2)
#     )

#     # Load risk index
#     risk = build_department_risk_index()

#     # Filter requested year
#     risk_year = risk[risk["annee"] == year]

#     # Merge geo + risk
#     gdf = geo.merge(
#         risk,
#         on="Code_departement",
#         how="left"
#     )

#     return gdf



# import geopandas as gpd
# import pandas as pd

# def build_geo_risk(year: int):
#     risk = pd.read_csv("data/processed/department_risk_index.csv")

#     risk_year = risk[risk["annee"] == year]

#     geo = gpd.read_file("data/raw/geo/departements.geojson")

#     # Normalize department code format
#     geo["Code_departement"] = geo["code"].astype(str).str.zfill(2)

#     gdf = geo.merge(
#         risk_year,
#         on="Code_departement",
#         how="left"
#     )

#     output_path = f"data/processed/risk_geo_{year}.geojson"
#     gdf.to_file(output_path, driver="GeoJSON")

#     return gdf

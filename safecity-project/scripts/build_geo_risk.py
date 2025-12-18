from data_processing.geo_processing import build_geo_risk

gdf = build_geo_risk(2022)
print(
    gdf[["Code_departement", "risk_score_norm", "risk_level"]].head()
)
print("Rows:", len(gdf))
# print(gdf[["Code_departement", "risk_score"]].head(10))
print("Missing risk scores:", gdf["risk_score_norm"].isna().sum())
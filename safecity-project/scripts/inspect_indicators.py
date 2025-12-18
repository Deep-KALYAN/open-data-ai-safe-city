import pandas as pd

df = pd.read_csv("data/processed/crime_summary.csv")

print("Number of unique indicators:", df["indicateur"].nunique())
print("\nIndicators list:\n")
print(df["indicateur"].sort_values().unique())
print("\nYear range:")
print(df["annee"].min(), "→", df["annee"].max())
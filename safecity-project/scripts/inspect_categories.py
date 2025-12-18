import pandas as pd

df = pd.read_csv("data/processed/crime_summary.csv")

print(df.groupby("crime_category")["nombre"].sum().sort_values(ascending=False))

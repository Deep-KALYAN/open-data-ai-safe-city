from data_processing.crime_processing import build_crime_summary

df = build_crime_summary()
print(df.head())
print("Rows:", len(df))

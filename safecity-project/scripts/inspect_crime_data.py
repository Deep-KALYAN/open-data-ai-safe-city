from data_ingestion.crime import load_crime_data

df = load_crime_data()
print(df.head())
print(df.columns.tolist())

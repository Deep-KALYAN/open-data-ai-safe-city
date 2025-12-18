from pipeline.extract import load_crimes, load_population, load_geo
from pipeline.transform import clean_crimes, aggregate_by_dept
from pipeline.enrich import add_population
from pipeline.validate import validate
from pathlib import Path

OUTPUT = Path("data/processed")
OUTPUT.mkdir(parents=True, exist_ok=True)

def main():
    crimes_raw = load_crimes()
    population = load_population()
    geo = load_geo()

    crimes_clean = clean_crimes(crimes_raw)
    crimes_agg = aggregate_by_dept(crimes_clean)
    crimes_final = add_population(crimes_agg, population)

    validate(crimes_final)

    crimes_final.to_parquet(OUTPUT / "crime_rates.parquet")
    geo.to_parquet(OUTPUT / "geo_departements.parquet")

    print("✅ Pipeline completed")

if __name__ == "__main__":
    main()

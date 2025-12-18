import pandas as pd

def add_population(crimes: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    df = crimes.merge(
        population,
        on=["departement", "year"],
        how="left"
    )
    df["crime_rate"] = (df["total_crimes"] / df["population"]) * 1000
    return df

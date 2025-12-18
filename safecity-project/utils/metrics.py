import pandas as pd

def compute_growth(df: pd.DataFrame, dept: str):
    dept_df = df[df["departement"] == dept]
    dept_df = dept_df.sort_values("year")
    dept_df["growth"] = dept_df["crime_rate"].pct_change() * 100
    return dept_df

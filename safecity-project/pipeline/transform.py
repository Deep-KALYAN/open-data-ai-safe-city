import pandas as pd

def clean_crimes(crimes_sheets: dict) -> pd.DataFrame:
    frames = []
    for year, df in crimes_sheets.items():
        df = df.copy()
        df["year"] = int(year[-4:])
        df.columns = df.columns.str.lower().str.strip()
        frames.append(df)

    crimes = pd.concat(frames, ignore_index=True)
    return crimes


def aggregate_by_dept(crimes: pd.DataFrame) -> pd.DataFrame:
    return (
        crimes
        .groupby(["departement", "year", "libelle_index"], as_index=False)
        .agg(total_crimes=("valeur", "sum"))
    )

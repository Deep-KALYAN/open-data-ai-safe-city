import plotly.express as px

def time_series(df, dept):
    data = df[df["departement"] == dept]
    return px.line(
        data,
        x="year",
        y="crime_rate",
        title=f"Crime rate over time — {dept}"
    )

def bar_top_crimes(df, year):
    data = df[df["year"] == year]
    return px.bar(
        data,
        x="libelle_index",
        y="total_crimes",
        title="Top crime categories"
    )

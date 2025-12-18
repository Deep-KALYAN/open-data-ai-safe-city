import plotly.express as px

def choropleth(df, geojson):
    return px.choropleth(
        df,
        geojson=geojson,
        locations="departement",
        color="crime_rate",
        featureidkey="properties.code",
        color_continuous_scale="Reds"
    )

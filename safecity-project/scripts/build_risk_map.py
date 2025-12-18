# scripts/build_risk_map.py
import folium
from data_processing.geo_processing import build_geo_risk


RISK_COLORS = {
    "Low": "#2ECC71",
    "Medium": "#F1C40F",
    "High": "#E74C3C",
}


def build_risk_map(year: int = 2022):
    print(f"🗺️ Building crime risk map for {year}...")

    gdf = build_geo_risk(year)

    # Center of France
    m = folium.Map(location=[46.5, 2.5], zoom_start=6, tiles="cartodbpositron")

    def style_function(feature):
        level = feature["properties"].get("risk_level", "Low")
        return {
            "fillColor": RISK_COLORS.get(level, "#BDC3C7"),
            "color": "black",
            "weight": 0.4,
            "fillOpacity": 0.7,
        }

    tooltip = folium.GeoJsonTooltip(
        fields=["DDEP_L_LIB", "risk_score_norm", "risk_level"],
        aliases=["Department", "Risk score", "Risk level"],
        localize=True,
    )

    folium.GeoJson(
        gdf,
        style_function=style_function,
        tooltip=tooltip,
    ).add_to(m)

    # ---- LEGEND ----
    legend_html = """
    <div style="
        position: fixed;
        bottom: 40px;
        left: 40px;
        width: 160px;
        background-color: white;
        border: 2px solid grey;
        z-index: 9999;
        font-size: 14px;
        padding: 10px;
    ">
    <b>Crime Risk Level</b><br>
    <i style="background:#2ECC71;width:12px;height:12px;display:inline-block"></i> Low<br>
    <i style="background:#F1C40F;width:12px;height:12px;display:inline-block"></i> Medium<br>
    <i style="background:#E74C3C;width:12px;height:12px;display:inline-block"></i> High
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    output_path = f"outputs/maps/department_risk_{year}.html"
    m.save(output_path)

    print(f"✅ Map saved to {output_path}")


if __name__ == "__main__":
    build_risk_map()


# import folium
# from data_processing.geo_processing import build_geo_risk


# def build_risk_map(year: int = 2022):
#     print(f"🗺️ Building crime risk map for {year}...")

#     gdf = build_geo_risk(year)

#     # Center of France
#     m = folium.Map(location=[46.6, 2.5], zoom_start=6, tiles="cartodbpositron")

#     folium.Choropleth(
#         geo_data=gdf,
#         data=gdf,
#         columns=["Code_departement", "risk_score"],
#         key_on="feature.properties.Code_departement",
#         fill_color="YlOrRd",
#         fill_opacity=0.8,
#         line_opacity=0.3,
#         legend_name="Crime Risk Score",
#         nan_fill_color="lightgray",
#     ).add_to(m)

#     # Tooltip
#     folium.GeoJson(
#         gdf,
#         tooltip=folium.GeoJsonTooltip(
#             fields=["Code_departement", "risk_score"],
#             aliases=["Department", "Risk score"],
#             localize=True,
#         ),
#     ).add_to(m)

#     output_path = f"outputs/maps/department_risk_{year}.html"
#     m.save(output_path)

#     print(f"✅ Map saved to {output_path}")


# if __name__ == "__main__":
#     build_risk_map()

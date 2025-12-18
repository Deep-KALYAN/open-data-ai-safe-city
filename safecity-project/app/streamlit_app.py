import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import geopandas as gpd
import pandas as pd
from data_processing.geo_processing import build_geo_risk
from ai.comparison_insights import generate_comparison_insight
from ai.safety_insights import generate_safety_insight


# import streamlit as st
# import geopandas as gpd
# import pandas as pd
# from data_processing.geo_processing import build_geo_risk

st.set_page_config(
    page_title="SafeCity – Crime Risk Dashboard",
    layout="wide",
)

st.title("🛡️ SafeCity – Crime Risk Dashboard")
st.markdown(
    """
    Interactive dashboard showing **crime risk levels per French department**  
    based on public open data (2016–2024).
    """
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("⚙️ Controls")

year = st.sidebar.slider(
    "Select year",
    min_value=2016,
    max_value=2024,
    value=2022,
    step=1,
)

# -------------------------
# Load data
# -------------------------
@st.cache_data
def load_geo_risk(year: int):
    return build_geo_risk(year)

gdf = load_geo_risk(year)

# -------------------------
# KPIs
# -------------------------
st.subheader(f"📊 Key Indicators – {year}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Departments",
        gdf["Code_departement"].nunique()
    )

with col2:
    st.metric(
        "Avg Risk Score",
        round(gdf["risk_score_norm"].mean(), 2)
    )

with col3:
    st.metric(
        "High Risk Areas",
        (gdf["risk_level"] == "High").sum()
    )

# -------------------------
# Map
# -------------------------
st.subheader("🗺️ Crime Risk Map")

# Convert GeoDataFrame to GeoJSON
geojson = gdf.to_json()

st.components.v1.html(
    open(f"outputs/maps/department_risk_{year}.html", "r", encoding="utf-8").read(),
    height=700,
)

# -------------------------
# Data table
# -------------------------
st.subheader("📋 Department Risk Table")

display_cols = [
    "Code_departement",
    "risk_score_norm",
    "risk_level",
]

st.dataframe(
    gdf[display_cols].sort_values("risk_score_norm", ascending=False),
    use_container_width=True,
)

# -------------------------
# AI Safety Insight
# -------------------------
st.subheader("🤖 AI Safety Insight")

# selected_dept = st.selectbox(
#     "Select a department",
#     gdf["Code_departement"].unique(),
# )
selected_dept = st.selectbox(
    "Select department",
    sorted(gdf["Code_departement"].unique())
)
dept_name = selected_dept

if st.button("Generate Safety Insight"):
    with st.spinner("Analyzing crime data..."):
        insight = generate_safety_insight(
            df_risk=gdf,
            dept_code=selected_dept,   # <-- MUST be dept_code
            year=year,
            provider="ollama",
        )   
    st.markdown(insight)

# -------------------------
# AI Comparison (D2)
# -------------------------
st.subheader("🆚 Compare Two Departments")

colA, colB = st.columns(2)

with colA:
    dept_a = st.selectbox(
        "Department A",
        gdf["Code_departement"].unique(),
        key="dept_a",
    )

with colB:
    dept_b = st.selectbox(
        "Department B",
        gdf["Code_departement"].unique(),
        key="dept_b",
    )

if dept_a != dept_b and st.button("Compare Departments"):
    with st.spinner("Comparing departments..."):
        comparison = generate_comparison_insight(
            df_risk=gdf,
            dept_a_code=dept_a,
            dept_a_name=dept_a,
            dept_b_code=dept_b,
            dept_b_name=dept_b,
            year=year,
            provider="ollama",
        )

    st.markdown(comparison)
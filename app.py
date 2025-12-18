# app.py
# Application SafeCity - Dashboard interactif avec Streamlit

import streamlit_folium as stf
import streamlit as st
import pandas as pd
from utils.data import load_merged_data, load_geojson
from utils.maps import SafeCityMapper
from utils.charts import SafeCityCharts
from utils.chatbot import SafeCityChatbot

# Configuration Streamlit
st.set_page_config(
    page_title="SafeCity - Tableau de bord sécurité",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏛️ SafeCity - Analyse de la Criminalité en France")
st.markdown("Dashboard interactif pour explorer les tendances criminelles par département")

# ===== CHARGEMENT DES DONNÉES =====
@st.cache_data
def load_data():
    """Charge les donnees une seule fois."""
    merged_df = load_merged_data()
    geojson_data = load_geojson()
    return merged_df, geojson_data

try:
    merged_df, geojson_data = load_data()
    st.success("✅ Données chargées avec succès")
except Exception as e:
    st.error(f"❌ Erreur chargement données : {str(e)}")
    st.stop()

# ===== SIDEBAR - FILTRES =====
st.sidebar.header("🔍 Filtres")

# Sélectionner l'année
years = sorted(merged_df["annee"].unique().tolist())
selected_year = st.sidebar.selectbox("Année", years, index=len(years)-1)

# Sélectionner type crime
crime_types = sorted(merged_df["indicateur"].unique().tolist())
selected_crime = st.sidebar.selectbox("Type de crime", ["Tous"] + crime_types)

# Sélectionner département(s)
departments = sorted(merged_df["nom_departement"].unique().tolist())
selected_dept = st.sidebar.multiselect("Département(s)", departments, default=[])

# ===== FILTRAGE DES DONNÉES =====
filtered_df = merged_df[merged_df["annee"] == selected_year].copy()

if selected_crime != "Tous":
    filtered_df = filtered_df[filtered_df["indicateur"] == selected_crime]

if selected_dept:
    filtered_df = filtered_df[filtered_df["nom_departement"].isin(selected_dept)]

# ===== AFFICHAGE PRINCIPAL =====
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total crimes", f"{filtered_df['nombre'].sum():,}")

with col2:
    st.metric("Départements", filtered_df["departement"].nunique())

with col3:
    st.metric("Types crimes", filtered_df["indicateur"].nunique())

with col4:
    avg_pop = filtered_df["population"].mean()
    st.metric("Pop. moyenne", f"{avg_pop:,.0f}")

# ===== TABS PRINCIPALES =====
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualisations", "🗺️ Cartographie", "💬 Chatbot", "📋 Données"])

# ===== TAB 1 : VISUALISATIONS =====
with tab1:
    st.subheader("Graphiques interactifs")
    
    charts = SafeCityCharts(merged_df)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("**Evolution temporelle**")
        if selected_dept:
            fig_timeline = charts.create_timeline_chart(
                department=selected_dept[0],
                crime_type=None if selected_crime == "Tous" else selected_crime
            )
        else:
            fig_timeline = charts.create_timeline_chart(
                crime_type=None if selected_crime == "Tous" else selected_crime
            )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col_b:
        st.write("**Top 10 Départements**")
        fig_top = charts.create_bar_chart_top_departments(
            year=selected_year,
            crime_type=None if selected_crime == "Tous" else selected_crime,
            top_n=10
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.write("**Comparaison départements**")
        if len(departments) >= 2:
            dept1 = st.selectbox("Département 1", departments)
            dept2 = st.selectbox("Département 2", [d for d in departments if d != dept1])
            fig_comparison = charts.create_comparison_chart(
                year=selected_year,
                dept1=dept1,
                dept2=dept2
            )
            st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col_d:
        st.write("**Distribution par type**")
        fig_pie = charts.create_pie_chart(
            year=selected_year,
            department=selected_dept[0] if selected_dept else None
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ===== TAB 2 : CARTOGRAPHIE =====
with tab2:
    st.subheader("Carte choroplèthe interactive")
    
    mapper = SafeCityMapper(merged_df, geojson_data)
    
    col_map1, col_map2 = st.columns([3, 1])
    
    with col_map1:
        map_obj = mapper.create_choropleth_map(
            year=selected_year,
            crime_type=None if selected_crime == "Tous" else selected_crime
        )
        stf.st_folium(map_obj, width=800, height=600)
    
    with col_map2:
        st.write("**Information carte**")
        st.info(f"""
        **Année** : {selected_year}
        **Crime** : {selected_crime}
        **Départements** : {filtered_df['departement'].nunique()}
        **Colorisation** : Taux de criminalité pour 100k habitants
        """)

# ===== TAB 3 : CHATBOT =====
with tab3:
    st.subheader("💬 Assistant IA SafeCity")
    
    # Initialiser le chatbot en session state
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = SafeCityChatbot(merged_df)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Afficher l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input utilisateur
    user_input = st.chat_input("Posez une question sur la criminalité en France...")
    
    if user_input:
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        # Obtenir la réponse du chatbot
        with st.spinner("🤖 Le chatbot réfléchit..."):
            response = st.session_state.chatbot.chat(user_input)
        
        # Ajouter la réponse
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.write(response)
    
    # Bouton reset conversation
    if st.button("🔄 Réinitialiser la conversation"):
        st.session_state.chatbot.reset()
        st.session_state.messages = []
        st.success("Conversation réinitialisée")
        st.rerun()

# ===== TAB 4 : DONNÉES =====
with tab4:
    st.subheader("📋 Données brutes")
    
    st.write(f"**Nombre de lignes affichées** : {len(filtered_df)}")
    
    # Afficher les données
    st.dataframe(
        filtered_df.sort_values("annee", ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Option téléchargement
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger CSV",
        data=csv,
        file_name=f"safecity_data_{selected_year}.csv",
        mime="text/csv"
    )

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
**SafeCity** - Dashboard d'analyse de criminalité en France
- Données : Ministère de l'Intérieur + INSEE (2020-2024)
- Visualisations : Plotly + Folium
- IA : Claude via LiteLLM
""")
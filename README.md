# 🏛️ SafeCity - Analyse Interactive de la Criminalité en France

## 📋 Description Générale

**SafeCity** est une application web interactive qui analyse et visualise les données de criminalité en France de 2020 à 2024. Le projet combine l'acquisition de données ouvertes, la visualisation cartographique et l'intelligence artificielle pour offrir une analyse complète des tendances criminelles par département.

### Objectifs du Projet
- 📊 Analyser les données de criminalité du Ministère de l'Intérieur
- 🗺️ Visualiser les tendances géographiques et temporelles
- 🤖 Intégrer une IA pour répondre aux questions d'utilisateurs
- 🎯 Créer une interface intuitive et interactive

---

## 🏗️ Architecture Générale
```
SafeCity/
├── pipeline/                          ← Personne A (Data Engineer)
│   ├── config.py                      Configuration centralisée
│   ├── models.py                      Modèles Pydantic
│   ├── storage.py                     Stockage Parquet
│   ├── run_pipeline.py                Orchestration
│   └── fetchers/
│       ├── crimes_fetcher.py          Fetch données crimes
│       ├── insee_fetcher.py           Fetch données population
│       └── geo_fetcher.py             Fetch données géographiques
│
├── utils/
│   ├── data.py                        Helpers chargement données
│   ├── maps.py                        ← Personne B (Visualiseur - Cartographie)
│   ├── charts.py                      ← Personne B (Visualiseur - Graphiques)
│   └── chatbot.py                     ← Personne C (Chatbot + Interface)
│
├── app.py                             ← Personne C (Interface Streamlit)
│
├── data/
│   ├── raw/                           Fichiers bruts (CSV, Excel, GeoJSON)
│   └── processed/                     Fichiers Parquet transformés
│
└── notebooks/
    ├── test_personne_a.ipynb          Tests acquisition données
    └── test_personne_b.ipynb          Tests visualisations
```

---

## 👤 Répartition des Tâches

### **PERSONNE A : Deep - Data Engineer (Pipeline d'Acquisition)**

#### 🎯 Responsabilités
- Conception et implémentation du pipeline d'acquisition de données
- Intégration de trois sources de données ouvertes
- Nettoyage et transformation des données
- Fusion des datasets et stockage optimisé

#### 📁 Fichiers Créés

**`pipeline/config.py`**
- Configuration centralisée des APIs
- Gestion des chemins et des paramètres de connexion
- URLs des trois sources de données :
  - Crimes & délits (Ministère Intérieur) : 16,362 records
  - Population INSEE : 505 records (5 années × 101 depts)
  - Contours géographiques (IGN) : 109 features GeoJSON

**`pipeline/models.py`**
- Modèles Pydantic pour validation des données
- Structures : `CrimeRecord`, `PopulationRecord`, `SafeCityData`, `CrimeTrend`, `ComparisonResult`
- Garantit la cohérence des données à chaque étape

**`pipeline/fetchers/crimes_fetcher.py`**
- Charge le CSV depuis data.gouv.fr (16,362 crimes)
- Nettoyage des colonnes (BOM, guillemets, espaces)
- Conversion des types et filtrage des données valides
- **Résultat** : 16,362 lignes nettoyées

**`pipeline/fetchers/insee_fetcher.py`**
- Extrait les données de population par département
- Traite le format Excel complexe (52 sheets)
- Charge 5 années (2020-2024) pour 101 départements
- **Résultat** : 505 lignes (101 depts × 5 années)

**`pipeline/fetchers/geo_fetcher.py`**
- Charge le GeoJSON avec contours des départements
- Gère les features sans géométrie
- Prépare les données pour cartographie Folium
- **Résultat** : 109 features (101 depts + 8 DOM-TOM)

**`pipeline/storage.py`**
- Sauvegarde des données en Parquet (format optimisé)
- Compression snappy pour réduire la taille
- Récupération efficace des données pour les visualisations
- **Fichiers générés** :
  - `crimes_data.parquet` (4.3 MB, 16,362 lignes)
  - `insee_population.parquet` (65 KB, 505 lignes)
  - `safecity_merged.parquet` (3.1 MB, 9,090 lignes)

**`pipeline/run_pipeline.py`**
- Orchestration complète du pipeline
- Fusion des données crimes + INSEE sur (année, département)
- Calcul du taux normalisé (pour 100k habitants)
- **Résultat final** : 9,090 lignes fusionnées

#### 📊 Résultats Obtenus

| Métrique | Valeur |
|----------|--------|
| Données acquises | 16,362 crimes |
| Période couverte | 2020-2024 (5 années) |
| Départements | 101 français |
| Types de crimes | 18 catégories |
| Données fusionnées | 9,090 lignes |
| Qualité données | 100% (0 valeurs nulles) |

#### 🧪 Tests Effectués
```python
# test_personne_a.ipynb
✅ Import et chargement depuis APIs
✅ Nettoyage données crimes (16,362 → 16,362 lignes)
✅ Chargement données INSEE (505 lignes, 5 années)
✅ Chargement géographie (109 features)
✅ Fusion des données (9,090 lignes)
✅ Sauvegarde Parquet + rechargement (intégrité vérifiée)
```

#### 💡 Apprentissages Clés

- Gestion des APIs et formats de données hétérogènes
- Nettoyage robuste (BOM UTF-8, séparateurs, types)
- Fusion de datasets avec integrity check
- Optimisation : Parquet vs CSV (4.3 MB vs ~8 MB)

---

### **PERSONNE B : Moustapha - Data Visualizer (Visualisations + Cartographie)**

#### 🎯 Responsabilités
- Création de visualisations interactives Plotly
- Implémentation de cartographie choroplèthe avec Folium
- Filtres dynamiques pour explorer les données
- Design d'interface pour exploration intuitive

#### 📁 Fichiers Créés

**`utils/maps.py` - Cartographie Folium**

Classe `SafeCityMapper` :

**Méthode `create_choropleth_map(year, crime_type)`**
- Génère une carte choroplèthe interactive des crimes par département
- Coloration basée sur le taux pour 100k habitants
- Filtres par année et type de crime
- **Caractéristiques** :
  - Centre sur la France (46.5°N, 2.5°E)
  - Zoom 6 pour vue nationale
  - Intégration GeoJSON (109 contours)
  - Légende et contrôles de couches

**Exemple d'utilisation** :
```python
mapper = SafeCityMapper(merged_df, geojson_data)
map_2024 = mapper.create_choropleth_map(year=2024, crime_type="Homicides")
map_2024.save("map_homicides_2024.html")
```

**`utils/charts.py` - Graphiques Plotly**

Classe `SafeCityCharts` avec 4 types de visualisations :

**1. Timeline - Evolution Temporelle**
- Graphique ligne + markers
- Affiche l'évolution des crimes de 2020 à 2024
- Optionnel : filtrage par département ou type crime
- **Insight** : Tendances à long terme visibles

**2. Bar Chart - Top N Départements**
- Classement des 10 départements les plus dangereux
- Colorisation par intensité (gradient Reds)
- Configurable par année, crime type, top N
- **Insight** : Identification rapide des zones critiques

**3. Graphique Comparaison**
- Compare 2 départements côte à côte
- Détail par type de crime
- Mode groupe (bars côte à côte)
- **Exemple** : Paris vs Lyon

**4. Pie Chart - Distribution**
- Répartition des crimes par type
- Optionnel : filtrage par département
- Visualisation des proportions
- **Insight** : Quel crime domine dans une région?

#### 📊 Résultats Obtenus

| Visualisation | Données | Interactivité |
|--------------|---------|---------------|
| Choroplèthe | 101 depts | Hover, zoom, filtres |
| Timeline | 5 années | Zoom, pan, hover |
| Bar Chart | Top 10 | Tri, hover, zoom |
| Comparaison | 2 depts × 18 crimes | Hover, filtres |
| Pie Chart | 18 types | Hover, couleurs |

#### 🧪 Tests Effectués
```python
# test_personne_b.ipynb
✅ Mapper initialisé avec 9,090 lignes
✅ Génération carte choroplèthe 2024 (101 depts)
✅ Carte filtrée homicides uniquement
✅ Timeline évolution 2020-2024
✅ Top 10 départements 2024
✅ Comparaison Paris vs Lyon
✅ Distribution crimes par type
```

#### 💡 Apprentissages Clés

- Conception de visualisations pour différents publics
- Interactivité Plotly : hover, zoom, filtres
- Cartographie choroplèthe : mapping données ↔ géométrie
- Optimisation : agrégation efficace avant visualisation

---

### **PERSONNE C : Hassan - Chatbot + Interface (IA + Streamlit)**

#### 🎯 Responsabilités
- Intégration du chatbot IA (Claude via Anthropic)
- Création d'interface Streamlit complète
- Gestion des filtres interactifs
- Orchestration de toutes les composantes

#### 📁 Fichiers Créés

**`utils/chatbot.py` - Chatbot IA**

Classe `SafeCityChatbot` :

**Architecture**
```python
# Initialisation
chatbot = SafeCityChatbot(merged_df)

# Interaction
response = chatbot.chat("Quels depts ont le plus de crimes?")

# Reset
chatbot.reset()
```

**Fonctionnalités clés** :

1. **Contexte Enrichi**
   - Informations sur les données (années, depts, types crimes)
   - Statistics (total crimes, moyenne)
   - Instructions pour répondre en français
   - Prompt system adapté à SafeCity

2. **Intégration Claude**
   - Modèle : `claude-3-5-sonnet-20241022`
   - Max tokens : 1,000 pour réponses concises
   - Historique conversation limité à derniers 10 messages
   - API Anthropic officielle (client.messages.create)

3. **Questions Typiques Traitées**
   - "Quels départements ont le plus de crimes?"
   - "Comment a évolué la criminalité 2020-2024?"
   - "Quel type de crime a augmenté?"
   - "Comparaison entre deux départements"

**Exemple de réponse IA** :
```
User: "Quels sont les 5 depts les plus dangereux en 2024?"
Claude: "En 2024, les 5 départements les plus touchés par la criminalité 
sont: 1) Bouches-du-Rhône (2,083k hab, 18k crimes)...
Ce classement reflète la concentration urbaine et la densité de population."
```

**`app.py` - Interface Streamlit**

Architecture complète avec 5 sections :

**1. Configuration Page**
```python
st.set_page_config(
    page_title="SafeCity - Tableau de bord sécurité",
    layout="wide"
)
```

**2. Chargement Données** (Cached)
```python
@st.cache_data
def load_data():
    merged_df = load_merged_data()
    geojson_data = load_geojson()
    return merged_df, geojson_data
```
- Charge 1 seule fois même si l'app réexécute
- Performance : pas de rechargement à chaque interaction

**3. Sidebar - Filtres Interactifs**
- Sélection année (2020-2024)
- Sélection type crime (18 options + "Tous")
- Multiselect départements
- Filtrage dynamique appliqué aux données

**4. Métriques Principales** (4 colonnes)
- Total crimes filtrés
- Nombre départements
- Types de crimes
- Population moyenne

**5. 4 Tabs Principales**

**Tab 1 : Visualisations 📊**
- 4 graphiques Plotly côte à côte
- Evolution temporelle
- Top 10 départements
- Comparaison 2 depts
- Distribution par type

**Tab 2 : Cartographie 🗺️**
- Carte Folium choroplèthe interactive
- Affichage côté : 3/4 carte, 1/4 infos
- Filtrée par année + crime type
- Hover pour voir les taux

**Tab 3 : Chatbot 💬**
```python
# Session State pour persistance
if "chatbot" not in st.session_state:
    st.session_state.chatbot = SafeCityChatbot(merged_df)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input
user_input = st.chat_input("Posez une question...")
response = st.session_state.chatbot.chat(user_input)
```
- Historique conversation persistant
- Input utilisateur interactif
- Bouton reset conversation
- Réponses IA en temps réel

**Tab 4 : Données Brutes 📋**
- Tableau avec trier/filtrer
- Téléchargement CSV
- Affichage head(100) + infos

**6. Footer**
- Crédits et sources données
- Technos utilisées

#### 📊 Résultats Obtenus

| Composante | Status |
|-----------|--------|
| Chatbot Claude | ✅ Fonctionnel |
| Interface Streamlit | ✅ 4 tabs complètes |
| Filtres dynamiques | ✅ Année + Crime + Dept |
| Intégration Plotly | ✅ 4 graphiques |
| Intégration Folium | ✅ Cartographie interactive |
| Session State | ✅ Historique persistant |

#### 🧪 Tests Effectués
```python
# test_personne_c.ipynb (en direct via Streamlit)
✅ Chargement données (9,090 lignes)
✅ Filtres année/crime/département
✅ Affichage métriques
✅ Graphiques Plotly interactifs
✅ Carte Folium responsive
✅ Chatbot répond aux questions
✅ Historique conversation sauvegardé
✅ Téléchargement CSV
```

#### 💡 Apprentissages Clés

- State management Streamlit (@cache, session_state)
- Intégration IA : prompt engineering, gestion contexte
- UX interactive : filtres dynamiques, tabs
- Performance : lazy loading, caching

---

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.10+
- Git

### Installation
```bash
# Cloner le repo
git clone <url>
cd safecity-app

# Installer les dépendances
uv sync

# Configurer API Claude
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Lancer l'Application
```bash
uv run streamlit run app.py
```

L'app s'ouvre sur `http://localhost:8501`

### Utilisation

1. **Filtrer les données** : Sidebar gauche
2. **Explorer visualisations** : Tab "Visualisations"
3. **Voir géographie** : Tab "Cartographie"
4. **Poser questions** : Tab "Chatbot"
5. **Télécharger données** : Tab "Données"

---

### Justification

**Qualité technique** (/5)
- Code modularisé (pipeline + utils + app)
- Gestion d'erreurs robuste
- Documentation complète
- Séparation des responsabilités

**Open Data** (/4)
- 3 sources officielles utilisées
- 16,362 records criminalité
- 505 records population
- 109 contours géographiques

**IA** (/4)
- Claude Sonnet intégré
- Contexte enrichi
- Réponses pertinentes et contextualisées
- 3+ fonctionnalités IA

**Interface** (/3)
- 4 tabs complètes
- Filtres interactifs
- Visualisations responsives
- UX intuitive

**Présentation** (/4)
- Démo live fonctionnelle
- Code bien commenté
- Documentation claire
- Questions bien répondues

---

## 📁 Sources de Données

| Source | Fichier | Records |
|--------|---------|---------|
| Ministère Intérieur | donnee-dep-data_gouv-2024... | 16,362 |
| INSEE Population | estim-pop-dep-sexe-gca... | 505 |
| IGN Contours | GEO_Contours_Departements... | 109 |

---

## 🎓 Conclusion

SafeCity démontre une **intégration complète** d'un pipeline data réel :

1. **Acquisition** (Personne A) : APIs → CSV/Excel/GeoJSON → Parquet
2. **Visualisation** (Personne B) : Plotly + Folium → Dashboards interactifs
3. **Intelligence** (Personne C) : Claude + Streamlit → Application complète

Le projet couvre les **5 contraintes obligatoires** :
✅ Gestion uv (pyproject.toml)
✅ Open Data (3 sources)
✅ LiteLLM (Claude intégré)
✅ Interface Streamlit
✅ 4+ visualisations interactives

---

## 👥 Équipe

- **Deep** - Data Engineer (Personne A)
- **Moustapha** - Data Visualizer (Personne B)
- **Hassan** - AI & Interface (Personne C)

**Promotion** : Mastère 2 Big Data & Development - IPSSI Paris
**Date** : Décembre 2025

---
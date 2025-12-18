import streamlit as st
from utils.data import load_crime_data, load_geo_data
from utils.charts import time_series, bar_top_crimes
from utils.chatbot import ask_question

st.set_page_config(page_title="SafeCity", layout="wide")

st.title("🏛️ SafeCity — Urban Security Dashboard")

df = load_crime_data()
geo = load_geo_data()

dept = st.selectbox("Select department", sorted(df["departement"].unique()))
year = st.slider("Year", int(df.year.min()), int(df.year.max()), 2021)

st.plotly_chart(time_series(df, dept), use_container_width=True)
st.plotly_chart(bar_top_crimes(df, year), use_container_width=True)

st.subheader("🤖 AI Analysis")
question = st.text_input("Ask a question about crime trends")

if question:
    context = df[df["departement"] == dept].to_string(index=False)
    answer = ask_question(question, context)
    st.write(answer)

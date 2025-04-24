import streamlit as st
from pages.dashboard import show_dashboard

st.set_page_config(page_title="Painel de Trading Esportivo", layout="wide")
st.title("Painel de Trading Esportivo")
st.markdown("Aqui você verá todos os gráficos e análises do seu desempenho.")

# Chamada do dashboard principal
show_dashboard()
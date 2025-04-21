
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Trading", layout="wide")
st.title("📊 Painel de Trading Esportivo")

uploaded_file = st.file_uploader("Carregue o Excel com os dados", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "Lucro / Prejuízo" in df.columns:
        df["Lucro / Prejuízo"] = pd.to_numeric(df["Lucro / Prejuízo"], errors="coerce")

        lucro_total = df["Lucro / Prejuízo"].sum()
        total_ops = len(df)
        winrate = (df["Lucro / Prejuízo"] > 0).mean() * 100

        st.metric("Lucro Total", f"R$ {lucro_total:,.2f}")
        st.metric("Taxa de Acerto", f"{winrate:.2f}%")
        st.metric("Nº Operações", total_ops)

        st.bar_chart(df["Lucro / Prejuízo"])
    else:
        st.error("Coluna 'Lucro / Prejuízo' não encontrada no arquivo.")
else:
    st.info("Envie um arquivo Excel para começar.")

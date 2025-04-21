import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel de Trading Esportivo", layout="wide")
st.title("📊 Painel de Trading Esportivo")

uploaded_file = st.file_uploader("📂 Envie seu Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="BASE DE DADOS PARA BI")
    df.columns = df.columns.str.strip()

    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    if "Profit / Loss" in df.columns:
        df["Profit / Loss"] = pd.to_numeric(df["Profit / Loss"], errors="coerce")

    df = df.dropna(subset=["Data", "Profit / Loss"])

    st.sidebar.header("Filtros")
    data_range = st.sidebar.date_input("Período", [df["Data"].min(), df["Data"].max()])
    ligas = st.sidebar.multiselect("Liga", df["Competição"].dropna().unique(), default=df["Competição"].dropna().unique())
    mercados = st.sidebar.multiselect("Mercado", df["Mercado"].dropna().unique(), default=df["Mercado"].dropna().unique())
    times = st.sidebar.multiselect("Times", pd.unique(df[["Time 1", "Time 2"]].values.ravel()), default=pd.unique(df[["Time 1", "Time 2"]].values.ravel()))

    df = df[(df["Data"] >= pd.to_datetime(data_range[0])) & (df["Data"] <= pd.to_datetime(data_range[1]))]
    df = df[df["Competição"].isin(ligas)]
    df = df[df["Mercado"].isin(mercados)]
    df = df[(df["Time 1"].isin(times)) | (df["Time 2"].isin(times))]

    st.metric("Lucro Total", f"R$ {df['Profit / Loss'].sum():,.2f}")
    st.metric("Taxa de Acerto", f"{(df['Profit / Loss'] > 0).mean() * 100:.2f}%")
    st.metric("Operações", df.shape[0])

    lucro_dia = df.groupby("Data")["Profit / Loss"].sum().reset_index()
    st.plotly_chart(px.bar(lucro_dia, x="Data", y="Profit / Loss", title="Lucro por Dia",
                           color="Profit / Loss", color_continuous_scale=["red", "green"]), use_container_width=True)
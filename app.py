import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel Trading", layout="wide")
st.title("📊 Painel de Trading Esportivo")

uploaded_file = st.file_uploader("📂 Envie seu arquivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="BASE DE DADOS PARA BI")
    df.columns = df.columns.str.strip().str.replace("\u00a0", " ").str.replace("
", " ")
    df.columns = df.columns.str.replace(r"\s+", " ", regex=True)

    # Visualizar colunas para debug
    st.write("🧾 Colunas detectadas:", df.columns.tolist())

    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    if "Profit / Loss" in df.columns:
        df["Profit / Loss"] = pd.to_numeric(df["Profit / Loss"], errors="coerce")

    df = df.dropna(subset=["Data", "Profit / Loss"])

    # Detectar colunas de times
    time_cols = [col for col in df.columns if "time" in col.lower()]
    st.write("🎯 Colunas possíveis de time:", time_cols)

    col_time_1 = time_cols[0] if len(time_cols) > 0 else None
    col_time_2 = time_cols[1] if len(time_cols) > 1 else None

    if not col_time_1 or not col_time_2:
        st.error("❌ Colunas de times não encontradas.")
    else:
        st.sidebar.header("Filtros")
        data_range = st.sidebar.date_input("Período", [df["Data"].min(), df["Data"].max()])
        ligas = st.sidebar.multiselect("Ligas", df["Competição"].dropna().unique(), default=df["Competição"].dropna().unique())
        mercados = st.sidebar.multiselect("Mercados", df["Mercado"].dropna().unique(), default=df["Mercado"].dropna().unique())
        times = st.sidebar.multiselect("Times", pd.unique(df[[col_time_1, col_time_2]].values.ravel()),
                                       default=pd.unique(df[[col_time_1, col_time_2]].values.ravel()))

        df = df[(df["Data"] >= pd.to_datetime(data_range[0])) & (df["Data"] <= pd.to_datetime(data_range[1]))]
        df = df[df["Competição"].isin(ligas)]
        df = df[df["Mercado"].isin(mercados)]
        df = df[(df[col_time_1].isin(times)) | (df[col_time_2].isin(times))]

        st.metric("Lucro Total", f"R$ {df['Profit / Loss'].sum():,.2f}")
        st.metric("Operações", df.shape[0])
        st.metric("Taxa de Acerto", f"{(df['Profit / Loss'] > 0).mean() * 100:.2f}%")

        lucro_dia = df.groupby("Data")["Profit / Loss"].sum().reset_index()
        st.plotly_chart(px.bar(lucro_dia, x="Data", y="Profit / Loss", title="Lucro por Dia",
                               color="Profit / Loss", color_continuous_scale=["red", "green"]), use_container_width=True)
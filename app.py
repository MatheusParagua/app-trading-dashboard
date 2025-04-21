
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel Trading Avançado", layout="wide")
st.title("📊 Painel de Trading Esportivo - Ajustado")

uploaded_file = st.file_uploader("📤 Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=2)
    df.rename(columns={"Tipo de jogo": "Tipo"}, inplace=True)

    df = df.dropna(subset=["Data", "Profit / Loss", "Mercado", "Tipo"])
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df = df.dropna(subset=["Data"])
    df["Mês"] = df["Data"].dt.to_period("M").astype(str)

    # Filtros
    with st.sidebar:
        st.header("🔎 Filtros")
        tipos = st.multiselect("Tipo de operação", df["Tipo"].unique(), default=df["Tipo"].unique())
        mercados = st.multiselect("Mercado", df["Mercado"].unique(), default=df["Mercado"].unique())
        datas = st.date_input("Período", [df["Data"].min(), df["Data"].max()])

    df_filtrado = df[
        (df["Tipo"].isin(tipos)) &
        (df["Mercado"].isin(mercados)) &
        (df["Data"] >= pd.to_datetime(datas[0])) &
        (df["Data"] <= pd.to_datetime(datas[1]))
    ]

    # KPIs
    lucro_total = df_filtrado["Profit / Loss"].sum()
    roi = (lucro_total / abs(df_filtrado["Profit / Loss"]).sum()) * 100
    acertos = (df_filtrado["Profit / Loss"] > 0).mean() * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Lucro Total", f"R$ {lucro_total:,.2f}")
    col2.metric("📈 ROI", f"{roi:.2f}%")
    col3.metric("🎯 Taxa de Acerto", f"{acertos:.2f}%")
    col4.metric("📊 Nº de Operações", len(df_filtrado))

    # Gráfico Lucro por Dia
    lucro_dia = df_filtrado.groupby("Data")["Profit / Loss"].sum().reset_index()
    fig1 = px.bar(lucro_dia, x="Data", y="Profit / Loss", title="Lucro por Dia",
                  color="Profit / Loss", color_continuous_scale=["red", "green"])
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico Lucro por Mercado
    lucro_mercado = df_filtrado.groupby("Mercado")["Profit / Loss"].sum().reset_index()
    fig2 = px.bar(lucro_mercado, x="Mercado", y="Profit / Loss", title="Lucro por Mercado",
                  color="Profit / Loss", color_continuous_scale=["red", "green"])
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico Lucro por Mês
    lucro_mes = df_filtrado.groupby("Mês")["Profit / Loss"].sum().reset_index()
    fig3 = px.bar(lucro_mes, x="Mês", y="Profit / Loss", title="Lucro por Mês",
                  color="Profit / Loss", color_continuous_scale=["red", "green"])
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Envie sua planilha para visualizar os dados.")

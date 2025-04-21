
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel Trading Avançado", layout="wide")
st.title("📊 Painel de Trading Esportivo - Completo")

uploaded_file = st.file_uploader("📤 Envie sua planilha Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=2)
    df.rename(columns={
        "Tipo de jogo": "Tipo",
        "Competição": "Liga",
        "Evento": "Time"
    }, inplace=True)

    df = df.dropna(subset=["Data", "Profit / Loss", "Mercado", "Tipo", "Liga", "Time"])
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df = df.dropna(subset=["Data"])
    df["Mês"] = df["Data"].dt.to_period("M").astype(str)

    # Filtros
    with st.sidebar:
        st.header("🔎 Filtros")
        datas = st.date_input("Período", [df["Data"].min(), df["Data"].max()])
        ligas = st.multiselect("Liga", df["Liga"].unique(), default=df["Liga"].unique())
        mercados = st.multiselect("Mercado", df["Mercado"].unique(), default=df["Mercado"].unique())
        times = st.multiselect("Times (Evento)", df["Time"].unique(), default=df["Time"].unique())

    df_f = df[
        (df["Data"] >= pd.to_datetime(datas[0])) &
        (df["Data"] <= pd.to_datetime(datas[1])) &
        (df["Liga"].isin(ligas)) &
        (df["Mercado"].isin(mercados)) &
        (df["Time"].isin(times))
    ]

    # KPIs
    lucro_total = df_f["Profit / Loss"].sum()
    roi = (lucro_total / abs(df_f["Profit / Loss"]).sum()) * 100 if len(df_f) else 0
    acertos = (df_f["Profit / Loss"] > 0).mean() * 100 if len(df_f) else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Lucro Total", f"R$ {lucro_total:,.2f}")
    col2.metric("📈 ROI", f"{roi:.2f}%")
    col3.metric("🎯 Acerto", f"{acertos:.2f}%")
    col4.metric("📊 Nº Operações", len(df_f))

    # Gráfico Lucro por Mês
    lucro_mes = df_f.groupby("Mês")["Profit / Loss"].sum().reset_index()
    fig1 = px.bar(lucro_mes, x="Mês", y="Profit / Loss", title="Lucro por Mês",
                  color="Profit / Loss", color_continuous_scale=["red", "green"])
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico Lucro por Mercado
    lucro_mercado = df_f.groupby("Mercado")["Profit / Loss"].sum().reset_index()
    fig2 = px.bar(lucro_mercado, x="Mercado", y="Profit / Loss", title="Lucro por Mercado",
                  color="Profit / Loss", color_continuous_scale=["red", "green"])
    st.plotly_chart(fig2, use_container_width=True)

    # Top 10 Times positivos e negativos
    st.subheader("🏆 Ranking de Times")
    lucro_times = df_f.groupby("Time")["Profit / Loss"].sum().sort_values(ascending=False)
    col_a, col_b = st.columns(2)
    col_a.markdown("### 🔝 10 Melhores Times")
    col_a.dataframe(lucro_times.head(10).reset_index())
    col_b.markdown("### 🔻 10 Piores Times")
    col_b.dataframe(lucro_times.tail(10).reset_index())

else:
    st.info("Por favor, envie sua planilha para visualizar os dados.")

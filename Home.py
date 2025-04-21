import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Trading Esportivo", layout="wide")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_excel("dados/RESULTADOS_2020.xlsx", sheet_name="BASE DE DADOS PARA BI")
    df["Data"] = pd.to_datetime(df["Data"])
    df["Profit / Loss"] = pd.to_numeric(df["Profit / Loss"], errors="coerce")
    return df

df = load_data()

# Filtros
st.sidebar.title("Filtros")
data_ini = st.sidebar.date_input("Data inicial", value=df["Data"].min())
data_fim = st.sidebar.date_input("Data final", value=df["Data"].max())
ligas = st.sidebar.multiselect("Ligas", options=df["Competição"].unique(), default=df["Competição"].unique())
mercados = st.sidebar.multiselect("Mercados", options=df["Mercado"].unique(), default=df["Mercado"].unique())
times = st.sidebar.multiselect("Times (Mandante ou Visitante)", options=pd.unique(df[["Mandante", "Visitante"]].values.ravel('K')), default=pd.unique(df[["Mandante", "Visitante"]].values.ravel('K')))

# Aplicar filtros
df_filtros = df[
    (df["Data"] >= pd.to_datetime(data_ini)) &
    (df["Data"] <= pd.to_datetime(data_fim)) &
    (df["Competição"].isin(ligas)) &
    (df["Mercado"].isin(mercados)) &
    (df["Mandante"].isin(times) | df["Visitante"].isin(times))
]

# KPIs
total_profit = df_filtros["Profit / Loss"].sum()
roi = 100 * df_filtros["Profit / Loss"].sum() / df_filtros["Stake"].sum()
taxa_acerto = 100 * (df_filtros["Profit / Loss"] > 0).sum() / len(df_filtros)

col1, col2, col3 = st.columns(3)
col1.metric("Lucro Total", f"R${total_profit:,.2f}")
col2.metric("ROI", f"{roi:.2f}%")
col3.metric("Taxa de Acerto", f"{taxa_acerto:.2f}%")

st.markdown("---")

# Gráficos
lucro_dia = df_filtros.groupby("Data")["Profit / Loss"].sum().reset_index()
fig1 = px.bar(lucro_dia, x="Data", y="Profit / Loss", title="Lucro por Dia", color="Profit / Loss", color_continuous_scale=["red", "green"])
st.plotly_chart(fig1, use_container_width=True)

lucro_mercado = df_filtros.groupby("Mercado")["Profit / Loss"].sum().sort_values().reset_index()
fig2 = px.bar(lucro_mercado, x="Mercado", y="Profit / Loss", title="Lucro por Mercado", color="Profit / Loss", color_continuous_scale=["red", "green"])
st.plotly_chart(fig2, use_container_width=True)

roi_mercado = df_filtros.groupby("Mercado").apply(lambda x: x["Profit / Loss"].sum() / x["Stake"].sum() * 100).reset_index(name="ROI")
fig3 = px.bar(roi_mercado, x="Mercado", y="ROI", title="ROI por Mercado", color="ROI", color_continuous_scale=["red", "green"])
st.plotly_chart(fig3, use_container_width=True)

# Ranking dos times
df_filtros["Time"] = df_filtros["Mandante"] + " x " + df_filtros["Visitante"]
ranking = df_filtros.groupby("Mandante")["Profit / Loss"].sum().sort_values(ascending=False).reset_index(name="Lucro")
melhores = ranking.head(10)
piores = ranking.tail(10).sort_values("Lucro")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🏆 Top 10 Times Mandantes")
    st.dataframe(melhores)

with col2:
    st.subheader("❌ Piores 10 Times Mandantes")
    st.dataframe(piores)

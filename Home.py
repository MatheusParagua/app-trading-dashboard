
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Trading", layout="wide")
st.title("📊 Painel de Trading Esportivo")

df = pd.read_csv("dados/Gestao_de_Banca_Rev_06.csv")
df.columns = df.columns.str.strip().str.replace("\u00a0", " ").str.replace(" ", "_")
df['Data'] = pd.to_datetime(df['Data'])

st.sidebar.header("Filtros")
ligas = st.sidebar.multiselect("Selecione a Liga", options=df['Competição'].unique(), default=df['Competição'].unique())
mercados = st.sidebar.multiselect("Selecione o Mercado", options=df['Mercado'].unique(), default=df['Mercado'].unique())

df_filtrado = df[(df['Competição'].isin(ligas)) & (df['Mercado'].isin(mercados))]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Lucro Total", f"R$ {df_filtrado['Profit / Loss'].sum():.2f}")
col2.metric("ROI (%)", f"{(df_filtrado['Profit / Loss'].sum() / df_filtrado['Stake'].sum()) * 100:.2f}%")
col3.metric("Taxa de Acerto", f"{(df_filtrado[df_filtrado['Profit / Loss'] > 0].shape[0] / df_filtrado.shape[0]) * 100:.2f}%")
col4.metric("Nº de Operações", df_filtrado.shape[0])

st.subheader("📅 Lucro por Dia")
lucro_dia = df_filtrado.groupby(df_filtrado['Data'].dt.date)['Profit / Loss'].sum()
st.bar_chart(lucro_dia)

st.subheader("🏟️ Lucro por Mercado")
lucro_mercado = df_filtrado.groupby('Mercado')['Profit / Loss'].sum().sort_values()
cores = ['#00FF00' if x >= 0 else '#FF0000' for x in lucro_mercado]
fig, ax = plt.subplots()
lucro_mercado.plot(kind='barh', color=cores, ax=ax)
st.pyplot(fig)

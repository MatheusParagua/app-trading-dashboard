
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Painel de Trading", layout="wide")
st.title("📈 Painel de Gestão de Trading Esportivo")

# Carrega o Excel com os nomes corretos
df = pd.read_excel("Gestao_de_Banca_Rev 06.xlsx", header=2)
df.dropna(subset=["Data", "Profit / Loss", "Mercado"], inplace=True)
df["Data"] = pd.to_datetime(df["Data"], errors='coerce')
df.dropna(subset=["Data"], inplace=True)

# Filtros
st.sidebar.header("Filtros")
data_inicio = st.sidebar.date_input("Data inicial", value=df["Data"].min().date())
data_fim = st.sidebar.date_input("Data final", value=df["Data"].max().date())
mercados = st.sidebar.multiselect("Mercados", options=df["Mercado"].unique(), default=df["Mercado"].unique())

# Aplicar filtros
filtro = (df["Data"].dt.date >= data_inicio) & (df["Data"].dt.date <= data_fim) & (df["Mercado"].isin(mercados))
df = df[filtro]

# Métricas
st.subheader("📊 Estatísticas")
st.metric("Total de operações", len(df))
st.metric("Lucro total", f"R$ {df['Profit / Loss'].sum():,.2f}")
st.metric("Taxa de acerto", f"{(df['Profit / Loss'] > 0).mean() * 100:.2f}%")
if "Stake" in df.columns:
    roi = df["Profit / Loss"].sum() / df["Stake"].sum() * 100
    st.metric("ROI", f"{roi:.2f}%")

# Gráfico de lucro ao longo do tempo
st.subheader("📈 Lucro acumulado")
df_sorted = df.sort_values("Data")
df_sorted["Lucro acumulado"] = df_sorted["Profit / Loss"].cumsum()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=df_sorted, x="Data", y="Lucro acumulado", ax=ax)
ax.axhline(0, linestyle="--", color="gray")
st.pyplot(fig)

# Gráfico de lucro por mercado
st.subheader("🏷️ Lucro médio por mercado")
lucro_mercado = df.groupby("Mercado")["Profit / Loss"].mean().sort_values(ascending=False)
st.bar_chart(lucro_mercado)

# Tabela de dados
st.subheader("📋 Operações filtradas")
st.dataframe(df, use_container_width=True)

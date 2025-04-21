
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Painel BI - Trading", layout="wide")
st.title("📈 Painel de Análise - Trading Esportivo")

# Carregar os dados da aba BASE DE DADOS PARA BI
df = pd.read_excel("Gestao_de_Banca_Rev 06.xlsx", sheet_name="BASE DE DADOS PARA BI")
df = df.dropna(subset=["Data", "Profit / Loss", "Mercado", "Tipo"])
df["Data"] = pd.to_datetime(df["Data"], errors='coerce')
df = df.dropna(subset=["Data"])

# Filtros laterais
st.sidebar.header("Filtros")
data_ini = st.sidebar.date_input("Data inicial", value=df["Data"].min().date())
data_fim = st.sidebar.date_input("Data final", value=df["Data"].max().date())
mercado = st.sidebar.multiselect("Mercado", df["Mercado"].unique(), default=df["Mercado"].unique())
df = df[(df["Data"].dt.date >= data_ini) & (df["Data"].dt.date <= data_fim) & (df["Mercado"].isin(mercado))]

# Gráfico 1: Lucro por dia
st.subheader("📅 Lucro por dia")
lucro_dia = df.groupby("Data")["Profit / Loss"].sum()
st.line_chart(lucro_dia)

# Gráfico 2: Lucro por mercado
st.subheader("💼 Lucro por mercado")
lucro_mercado = df.groupby("Mercado")["Profit / Loss"].sum().sort_values()
st.bar_chart(lucro_mercado)

# Gráfico 3: ROI por mercado
if "Stake" in df.columns:
    st.subheader("📈 ROI por mercado")
    roi_mercado = df.groupby("Mercado").apply(lambda x: x["Profit / Loss"].sum() / x["Stake"].sum() * 100)
    st.bar_chart(roi_mercado)

# Gráfico 4: Taxa de acerto por competição
if "Competição" in df.columns:
    st.subheader("🥇 Taxa de acerto por competição")
    acertos = df[df["Profit / Loss"] > 0].groupby("Competição").size()
    total = df.groupby("Competição").size()
    taxa_acerto = (acertos / total * 100).fillna(0)
    st.bar_chart(taxa_acerto)

# Gráfico 5: Pizza por tipo de operação
st.subheader("🥧 Distribuição por Tipo de Operação")
tipo_contagem = df["Tipo"].value_counts()
fig, ax = plt.subplots()
ax.pie(tipo_contagem, labels=tipo_contagem.index, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Gráfico 6: Lucro por mês/ano
st.subheader("📆 Lucro por mês/ano")
df["AnoMes"] = df["Data"].dt.to_period("M").astype(str)
lucro_mes = df.groupby("AnoMes")["Profit / Loss"].sum()
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(x=lucro_mes.index, y=lucro_mes.values, ax=ax2)
ax2.set_ylabel("Lucro")
ax2.set_xlabel("Mês/Ano")
plt.xticks(rotation=45)
st.pyplot(fig2)

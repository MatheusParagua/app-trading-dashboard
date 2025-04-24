
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados
df = pd.read_excel("Dados de Trading.xlsx")

# Corrige a conversão de datas
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Data'])

# Título
st.image("PARAGUATRADER - LOGO.png", width=150)
st.title("Painel ParaguaTrader")

# Exibe os dados
st.subheader("Dados brutos")
st.dataframe(df)

# Gráfico de lucro por dia
st.subheader("Lucro por dia")
lucro_por_dia = df.groupby(df['Data'].dt.date)['Profit / Loss'].sum()
fig, ax = plt.subplots()
colors = ['green' if x >= 0 else 'red' for x in lucro_por_dia]
lucro_por_dia.plot(kind='bar', ax=ax, color=colors)
st.pyplot(fig)

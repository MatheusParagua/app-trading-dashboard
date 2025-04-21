
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Trading", layout="wide")
st.title("📈 Painel de Trading Esportivo - Resolvido")

uploaded_file = st.file_uploader("Envie sua planilha Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=2)
        df.rename(columns={
            "Tipo de jogo": "Tipo",
        }, inplace=True)

        df = df.dropna(subset=["Data", "Profit / Loss", "Mercado", "Tipo"])
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
        df = df.dropna(subset=["Data"])
        df["Mês"] = df["Data"].dt.to_period("M").astype(str)

        st.success("✅ Planilha carregada com sucesso!")

        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Lucro Total", f"R$ {df['Profit / Loss'].sum():,.2f}")
        col2.metric("Taxa de Acerto", f"{(df['Profit / Loss'] > 0).mean()*100:.2f}%")
        col3.metric("Nº de Operações", len(df))

        st.markdown("### 📅 Lucro por Dia")
        st.line_chart(df.groupby("Data")["Profit / Loss"].sum())

        st.markdown("### 💼 Lucro por Mercado")
        st.bar_chart(df.groupby("Mercado")["Profit / Loss"].sum().sort_values())

        st.markdown("### 📈 Lucro por Mês")
        st.bar_chart(df.groupby("Mês")["Profit / Loss"].sum())

        st.markdown("### 🥧 Distribuição por Tipo de Operação")
        fig, ax = plt.subplots()
        df["Tipo"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao carregar a planilha: {e}")
else:
    st.info("Por favor, envie sua planilha Excel para iniciar a análise.")

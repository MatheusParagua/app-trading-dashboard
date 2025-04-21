
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Painel de Trading Esportivo", layout="wide")
st.title("📊 Painel de Trading Esportivo")
st.markdown("Carregue o Excel com os dados")

uploaded_file = st.file_uploader("Arraste o arquivo aqui", type=["xlsx"])

df.columns = df.columns.str.strip().str.replace("\u00a0", " ").str.replace("\n", " ").str.replace("\r", " ")
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Base de dados para BI")
        st.success("✅ Arquivo carregado com sucesso!")

        # Corrige possíveis espaços ou quebras nos nomes das colunas
        df.columns = df.columns.str.strip()

        if 'Profit / Loss' not in df.columns:
            st.error("Coluna 'Profit / Loss' não encontrada na aba 'Base de dados para BI'.")
        else:
            total_profit = df['Profit / Loss'].sum()
            st.subheader("📌 Visão Geral dos Dados")
            st.metric("Lucro Total", f"R$ {total_profit:,.2f}")

            # Gráfico de lucro por dia
            if 'Data' in df.columns:
                df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
                lucro_por_dia = df.groupby('Data')['Profit / Loss'].sum()
                fig, ax = plt.subplots()
                lucro_por_dia.plot(kind='bar', ax=ax)
                ax.set_title("Lucro por Dia")
                ax.set_ylabel("R$")
                st.pyplot(fig)
            else:
                st.warning("Coluna 'Data' não encontrada para exibir gráfico.")
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

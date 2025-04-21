
import streamlit as st
import pandas as pd

st.title("Painel de Operações de Trading Esportivo")
uploaded_file = st.file_uploader("Faça upload do seu arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="BASE DE DADOS PARA BI")
        if "Data" not in df.columns:
            st.error("Coluna 'Data' não encontrada na aba 'BASE DE DADOS PARA BI'.")
        else:
            st.success("Arquivo carregado com sucesso!")
            st.dataframe(df.head())
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")

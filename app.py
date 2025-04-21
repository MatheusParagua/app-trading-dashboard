
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor de Trading", layout="wide")

st.title("📊 Gestor de Trading")
st.markdown("Faça o upload do seu arquivo de operações em Excel (.xlsx) para ver a análise.")

uploaded_file = st.file_uploader("Upload do arquivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Arquivo carregado com sucesso!")
    
    st.subheader("📄 Visualização dos Dados")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Estatísticas Gerais")
    st.write("Número de operações:", len(df))
    st.write("Lucro/Prejuízo total:", df['Lucro/Prejuízo'].sum())
    st.write("Lucro médio por operação:", df['Lucro/Prejuízo'].mean())

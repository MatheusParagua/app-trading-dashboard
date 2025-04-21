
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Painel de Operações de Trading Esportivo")

uploaded_file = st.file_uploader("Faça upload do seu arquivo Excel", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        # Corrigir o nome da coluna de data
        df.columns = df.columns.str.strip()
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
        else:
            st.error("Coluna 'Data' não encontrada no arquivo.")
            st.stop()

        # Filtros laterais
        st.sidebar.header("Filtros")
        ligas = st.sidebar.multiselect("Competição", options=df['Competição'].unique(), default=df['Competição'].unique())
        mercados = st.sidebar.multiselect("Mercado", options=df['Mercado'].unique(), default=df['Mercado'].unique())
        times = st.sidebar.multiselect("Times", options=pd.concat([df['Mandante'], df['Visitante']]).unique())

        df_filtrado = df[
            (df['Competição'].isin(ligas)) &
            (df['Mercado'].isin(mercados)) &
            ((df['Mandante'].isin(times)) | (df['Visitante'].isin(times)) if times else True)
        ]

        st.subheader("KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Operações", len(df_filtrado))
        col2.metric("Lucro Total", f"R$ {df_filtrado['Profit / Loss'].sum():,.2f}")
        col3.metric("ROI Médio", f"{(df_filtrado['Profit / Loss'].sum() / df_filtrado['Stake'].sum()) * 100:.2f}%")

        # Gráficos
        st.subheader("Gráficos")

        lucro_por_dia = df_filtrado.groupby(df_filtrado['Data'].dt.date)['Profit / Loss'].sum().reset_index()
        fig_dia = px.bar(lucro_por_dia, x='Data', y='Profit / Loss', title="Lucro por Dia",
                         color='Profit / Loss', color_continuous_scale=['red', 'green'])
        st.plotly_chart(fig_dia, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")


import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trading Dashboard", layout="wide")

st.title("Painel de Operações de Trading Esportivo")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Faça upload do seu arquivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Normaliza nome das colunas
        df.columns = df.columns.str.strip()

        st.sidebar.header("Filtros")
        data_selecionada = st.sidebar.multiselect("Data", sorted(df["Date"].dropna().unique()))
        liga_selecionada = st.sidebar.multiselect("Liga", sorted(df["Competition"].dropna().unique()))
        mercado_selecionado = st.sidebar.multiselect("Mercado", sorted(df["Market"].dropna().unique()))
        times_selecionados = st.sidebar.multiselect("Times", sorted(set(df["Home Team"].dropna().unique()).union(set(df["Away Team"].dropna().unique()))))

        if data_selecionada:
            df = df[df["Date"].isin(data_selecionada)]
        if liga_selecionada:
            df = df[df["Competition"].isin(liga_selecionada)]
        if mercado_selecionado:
            df = df[df["Market"].isin(mercado_selecionado)]
        if times_selecionados:
            df = df[df["Home Team"].isin(times_selecionados) | df["Away Team"].isin(times_selecionados)]

        df["ROI"] = df["Profit / Loss"] / df["Stake"]
        df["Acerto"] = df["Profit / Loss"].apply(lambda x: 1 if x > 0 else 0)
        lucro_total = df["Profit / Loss"].sum()
        roi_total = df["ROI"].mean()
        taxa_acerto = df["Acerto"].mean()
        lucro_medio_mercado = df.groupby("Market")["Profit / Loss"].mean().mean()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Lucro Total", f"R$ {lucro_total:.2f}")
        col2.metric("ROI Médio", f"{roi_total:.2%}")
        col3.metric("Taxa de Acerto", f"{taxa_acerto:.2%}")
        col4.metric("Lucro Médio por Mercado", f"R$ {lucro_medio_mercado:.2f}")

        st.subheader("Lucro por Dia")
        lucro_por_dia = df.groupby("Date")["Profit / Loss"].sum()
        st.bar_chart(lucro_por_dia)

        st.subheader("Lucro por Mercado")
        lucro_por_mercado = df.groupby("Market")["Profit / Loss"].sum().sort_values()
        st.bar_chart(lucro_por_mercado)

        st.subheader("ROI por Mercado")
        roi_por_mercado = df.groupby("Market")["ROI"].mean().sort_values()
        st.bar_chart(roi_por_mercado)

        st.subheader("Taxa de Acerto por Competição")
        acerto_por_competicao = df.groupby("Competition")["Acerto"].mean().sort_values()
        st.bar_chart(acerto_por_competicao)

        st.subheader("Distribuição por Tipo de Operação")
        tipo_operacao = df["Market"].value_counts()
        st.pyplot(tipo_operacao.plot.pie(autopct='%1.1f%%', figsize=(6, 6)).get_figure())

        st.subheader("Lucro por Mês/Ano")
        df["AnoMes"] = pd.to_datetime(df["Date"]).dt.to_period("M")
        lucro_por_mes = df.groupby("AnoMes")["Profit / Loss"].sum()
        st.line_chart(lucro_por_mes)

        st.subheader("Ranking de Times")
        df["Time"] = df["Home Team"].where(df["Profit / Loss"] > 0, df["Away Team"])
        ranking_times = df.groupby("Time")["Profit / Loss"].sum().sort_values(ascending=False)
        col1, col2 = st.columns(2)
        col1.write("🏆 Top 10 Times")
        col1.bar_chart(ranking_times.head(10))
        col2.write("👎 Piores 10 Times")
        col2.bar_chart(ranking_times.tail(10))

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

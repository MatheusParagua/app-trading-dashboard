import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trading Dashboard", layout="wide")

st.title("📊 Trading Esportivo - Painel de Análise")

uploaded_file = st.file_uploader("📂 Carregue seu arquivo Excel com as operações", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.success("Arquivo carregado com sucesso!")
    st.subheader("📌 Visão Geral dos Dados")

    # Conversão de datas se existir coluna de data
    if "Date" in df.columns or "Data" in df.columns:
        date_col = "Date" if "Date" in df.columns else "Data"
        df[date_col] = pd.to_datetime(df[date_col])
        df["Ano"] = df[date_col].dt.year
        df["Mês"] = df[date_col].dt.strftime("%Y-%m")

    # KPIs
    total_profit = df['Profit / Loss'].sum()
    roi = (total_profit / df['Stake'].sum()) * 100 if 'Stake' in df.columns else 0
    winrate = (df[df['Profit / Loss'] > 0].shape[0] / df.shape[0]) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Lucro Total", f"R$ {total_profit:.2f}")
    col2.metric("📈 ROI", f"{roi:.2f}%")
    col3.metric("✅ Taxa de Acerto", f"{winrate:.2f}%")

    # Gráficos
    st.subheader("📅 Lucro por Dia")
    if "Date" in df.columns or "Data" in df.columns:
        lucro_dia = df.groupby(df[date_col].dt.date)['Profit / Loss'].sum().reset_index()
        fig = px.bar(lucro_dia, x=date_col, y='Profit / Loss', title="Lucro por Dia",
                     color='Profit / Loss', color_continuous_scale=["red", "green"])
        st.plotly_chart(fig, use_container_width=True)

    if 'Market' in df.columns:
        st.subheader("🏟️ Lucro por Mercado")
        lucro_mercado = df.groupby('Market')['Profit / Loss'].sum().reset_index()
        fig2 = px.bar(lucro_mercado, x='Market', y='Profit / Loss', title="Lucro por Mercado",
                      color='Profit / Loss', color_continuous_scale=["red", "green"])
        st.plotly_chart(fig2, use_container_width=True)

    if 'Competition' in df.columns:
        st.subheader("🏆 Taxa de Acerto por Competição")
        comp = df.groupby('Competition').apply(lambda x: (x['Profit / Loss'] > 0).sum() / len(x) * 100).reset_index(name='Winrate')
        fig3 = px.bar(comp, x='Competition', y='Winrate', title="Taxa de Acerto por Competição")
        st.plotly_chart(fig3, use_container_width=True)

    if 'Type' in df.columns:
        st.subheader("🥧 Distribuição por Tipo de Operação")
        fig4 = px.pie(df, names='Type', title="Distribuição por Tipo")
        st.plotly_chart(fig4, use_container_width=True)

    if "Mês" in df.columns:
        st.subheader("📆 Lucro por Mês")
        lucro_mes = df.groupby("Mês")["Profit / Loss"].sum().reset_index()
        fig5 = px.bar(lucro_mes, x="Mês", y="Profit / Loss", title="Lucro por Mês",
                      color='Profit / Loss', color_continuous_scale=["red", "green"])
        st.plotly_chart(fig5, use_container_width=True)
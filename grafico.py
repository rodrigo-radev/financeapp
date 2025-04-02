import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
def carregar_dados():
    arquivo = st.file_uploader("Carregar CSV", type=["csv"])
    if arquivo is not None:
        df = pd.read_csv(arquivo, sep=';', decimal=',')
        df['VALOR'] = df['VALOR'].str.replace(',', '.').astype(float)  # Converte para float
        df['DATA CAIXA'] = pd.to_datetime(df['DATA CAIXA'], format='%Y-%m-%d')
        df['Mês/Ano'] = df['DATA CAIXA'].dt.strftime('%Y-%m')
        df['Tipo'] = df['VALOR'].apply(lambda x: 'Receita' if x > 0 else 'Gasto')  # Define tipo de transação
        return df
    return None

st.title("Análise de Receitas e Gastos por Categoria")
df = carregar_dados()

if df is not None:
    # Criar seleção de mês
    meses_disponiveis = df['Mês/Ano'].unique()
    mes_selecionado = st.selectbox("Selecione o mês", sorted(meses_disponiveis, reverse=True))
    
    # Filtrar pelo mês selecionado
    df_filtrado = df[df['Mês/Ano'] == mes_selecionado]
    
    # Criar DataFrames separados para receitas e gastos
    df_receitas = df_filtrado[df_filtrado['Tipo'] == 'Receita'].groupby('CATEGORIA')['VALOR'].sum().reset_index()
    df_gastos = df_filtrado[df_filtrado['Tipo'] == 'Gasto'].groupby('CATEGORIA')['VALOR'].sum().reset_index()
    df_gastos['VALOR'] = df_gastos['VALOR'].abs()  # Garante que os valores de gastos sejam positivos
    
    # Criar gráficos separados
    if not df_receitas.empty:
        fig_receitas = px.bar(df_receitas, x='CATEGORIA', y='VALOR', color='CATEGORIA',
                              title=f'Receitas por Categoria - {mes_selecionado}',
                              labels={'VALOR': 'Valor (R$)', 'CATEGORIA': 'Categoria'})
        st.plotly_chart(fig_receitas)
    else:
        st.write("Nenhuma receita encontrada para este mês.")
    
    if not df_gastos.empty:
        fig_gastos = px.bar(df_gastos, x='CATEGORIA', y='VALOR', color='CATEGORIA',
                            title=f'Gastos por Categoria - {mes_selecionado}',
                            labels={'VALOR': 'Valor (R$)', 'CATEGORIA': 'Categoria'})
        st.plotly_chart(fig_gastos)
    else:
        st.write("Nenhum gasto encontrado para este mês.")


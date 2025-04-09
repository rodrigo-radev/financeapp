import json, os, csv
import streamlit as st
import pandas as pd

def voltar():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state.page = "home"

def salva_json(json_file_path, result):
    try:
        # Salvar o JSON gerado em um arquivo
        with open(json_file_path, "w") as json_file:
            json.dump(result, json_file)
    except Exception as e:
        st.write(f"Erro ao salvar o arquivo JSON. Tente novamente.\n{e}")

def to_csv(itens, file_path,reset=False):
    if not itens:
        print("A lista de itens está vazia. Nenhum dado será salvo.")
        return

    if(reset):
        try:
            os.remove(file_path)
        except:
            pass

        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=itens[0].keys())
            
            writer.writeheader()
            # Escreve os dados da lista de itens
            for item in itens:
                writer.writerow(item)
    else:
        try:

            # Verifica se o arquivo já existe
            file_exists = os.path.exists(file_path)

            # Escreve os dados no arquivo CSV
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=itens[0].keys())
                
                # Escreve o cabeçalho apenas se o arquivo não existir
                if not file_exists:
                    writer.writeheader()
                
                # Escreve os dados da lista de itens
                for item in itens:
                    writer.writerow(item)
        except Exception as e:
            print(f"Erro ao escrever no arquivo CSV: {e}")

def unificar(auto,manual):
    import perfil
    unificado = perfil.Itens()
    unificado.extend(auto)
    unificado.extend(manual)
    return unificado

def exibir_database():
    st.title("Database Completa")
    cont1= st.container()
    with cont1:
        st.write("Aqui você pode visualizar a base de dados completa.")
        import perfil

        auto = perfil.Itens()
        manual = perfil.Itens()

        auto.from_csv("./database/auto.csv")
        manual.from_csv("./database/entrada_manual.csv")

        unificado = unificar(auto,manual)

        columns = st.columns(3)
        mostrar,teste,classificado = False, False, False
        with columns[0]:
            if st.button("Mostrar JSON",key="json"):
                teste = True
                mostrar = True
        with columns[1]:
            if st.button("Mostrar Dataframe",key="dataframe"):
                teste = False
                mostrar = True

        if mostrar and teste:
            st.write(unificado.to_dict())
        elif mostrar and not teste:
            st.write(pd.DataFrame(unificado.to_dict()))

        with columns[2]:
            if st.button("Classificar",'classificar'):
                classificar_itens(unificado)
                st.warning("Classificado!")
                classificado = True
    if classificado:
        show = perfil.Itens()
        show.from_csv('./database/classificado.csv')
        st.write(pd.DataFrame(show.to_dict()))
    st.button("Voltar", on_click=voltar,key="voltar")

def classificar_itens(itens):
    import skttest4 as sk
    for i in itens.get_all():
        sk.classificacao(i)
    try:
        to_csv(itens.to_dict(),"./database/classificado.csv", True)
    except Exception as e:
        st.write(e)
        df = itens.to_json()
        df = pd.read_json(df)
        st.write(df)

def export_excel(file,to_file):
    if st.button("Exportar",key='exportar'):

            expo = pd.read_csv(file)
            expo.to_excel(to_file)
            st.success("Arquivo exportado")

            with open(to_file, 'rb') as f:
                st.download_button(label="Download",data=f,file_name='export_lancamento.xlsx',mime='xlsx')

def exibir_graficos():
    import plotly.express as px
    st.title("Gráficos")
    st.write("Aqui você pode visualizar gráficos da base de dados.")
    import perfil

    auto = perfil.Itens()
    auto.from_csv("./database/export.csv")
    manual = perfil.Itens()
    manual.from_csv("./database/entrada_manual.csv")

    unificado = unificar(auto, manual)
    
    # Converter para DataFrame
    df = pd.DataFrame.from_dict(unificado.to_dict())
    df['VALOR'] = pd.to_numeric(df['VALOR'])  # Converte para float
    df['DATA CAIXA'] = pd.to_datetime(df['DATA CAIXA'],dayfirst=True)
    df['Mês/Ano'] = df['DATA CAIXA'].dt.strftime('%Y-%m')
    df['Tipo'] = df['VALOR'].apply(lambda x: 'Receita' if x > 0 else 'Gasto')  # Define tipo de transação


    # Criar seleção de mês
    meses_disponiveis = df['Mês/Ano'].unique()
    mes_selecionado = st.selectbox("Selecione o mês", sorted(meses_disponiveis, reverse=True),index=16)
    
    # Filtrar pelo mês selecionado
    df_filtrado = df[df['Mês/Ano'] == mes_selecionado]
    
    # Criar DataFrames separados para receitas e gastos
    df_receitas = df_filtrado[df_filtrado['Tipo'] == 'Receita'].groupby('CATEGORIA')['VALOR'].sum().reset_index()
    df_gastos = df_filtrado[df_filtrado['Tipo'] == 'Gasto'].groupby('CATEGORIA')['VALOR'].sum().reset_index()
    df_gastos['VALOR'] = df_gastos['VALOR'].abs()  # Garante que os valores de gastos sejam positivos
    
    # Calcular resumo financeiro do mês
    total_receitas = df_receitas['VALOR'].sum() if not df_receitas.empty else 0
    total_gastos = df_gastos['VALOR'].sum() if not df_gastos.empty else 0
    saldo = total_receitas - total_gastos

    # Exibir resumo financeiro
    st.subheader(f"Resumo Financeiro - {mes_selecionado}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
    col2.metric("Total Gastos", f"R$ {total_gastos:,.2f}")
    col3.metric("Saldo do Mês", f"R$ {saldo:,.2f}", delta=f"R$ {saldo:,.2f}")

    # Exibir tabela com as categorias de maior receita e maior gasto
    st.subheader("🏆 Top 5 Categorias com Maior Receita")
    if not df_receitas.empty:
        st.write(df_receitas.sort_values(by="VALOR", ascending=False).head(5))
    else:
        st.write("Nenhuma receita encontrada para este mês.")

    st.subheader("💰 Top 5 Categorias com Maior Gasto")
    if not df_gastos.empty:
        st.write(df_gastos.sort_values(by="VALOR", ascending=False).head(5))
    else:
        st.write("Nenhum gasto encontrado para este mês.")
    
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

    st.header("🔎 Análise por Subcategoria")

    # Criar seleção de categoria para análise detalhada
    from perfil import Dados
    Dados = perfil.Dados()
    categorias_disponiveis = Dados.get_categorias_values()
    categoria_analisada = st.selectbox("📂 Escolha uma categoria para ver detalhes das subcategorias", ["Nenhuma"] + list(categorias_disponiveis))

    if categoria_analisada != "Nenhuma":
        df_sub = df[df['CATEGORIA'] == categoria_analisada]

        # Criar DataFrames separados para receitas e gastos por subcategoria
        df_receitas_sub = df_sub[df_sub['Tipo'] == 'Receita'].groupby('SUBCATEGORIA')['VALOR'].sum().reset_index()
        df_gastos_sub = df_sub[df_sub['Tipo'] == 'Gasto'].groupby('SUBCATEGORIA')['VALOR'].sum().reset_index()
        df_gastos_sub['VALOR'] = df_gastos_sub['VALOR'].abs()  # Garante que os valores de gastos sejam positivos

        # Criar gráfico de barras comparativo para as subcategorias
        df_subcategorias = df_sub.groupby(['SUBCATEGORIA', 'Tipo'])['VALOR'].sum().reset_index()
        if not df_subcategorias.empty:
            fig_subcategorias = px.bar(df_subcategorias, x='SUBCATEGORIA', y='VALOR', color='Tipo', barmode='group',
                                    title=f"📊 Receitas e Gastos por Subcategoria - {categoria_analisada}")
            st.plotly_chart(fig_subcategorias)

        # Criar gráficos de pizza para distribuição de receitas e gastos
        col1, col2 = st.columns(2)

        with col1:
            if not df_gastos_sub.empty:
                fig_pizza_gastos = px.pie(df_gastos_sub, values='VALOR', names='SUBCATEGORIA',
                                        title=f"💰 Gastos por Subcategoria - {categoria_analisada}", hole=0.4)
                st.plotly_chart(fig_pizza_gastos)

        with col2:
            if not df_receitas_sub.empty:
                fig_pizza_receitas = px.pie(df_receitas_sub, values='VALOR', names='SUBCATEGORIA',
                                            title=f"📈 Receitas por Subcategoria - {categoria_analisada}", hole=0.4)
                st.plotly_chart(fig_pizza_receitas)

    st.button("Voltar", on_click=voltar, key="voltar")
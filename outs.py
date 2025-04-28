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
    import streamlit as st
    import pandas as pd
    import perfil

    st.title("Gráficos")
    st.write("Aqui você pode visualizar gráficos da base de dados.")

    df = pd.read_csv("database/export.csv")
    df['VALOR'] = pd.to_numeric(df['VALOR'])
    df['DATA CAIXA'] = pd.to_datetime(df['DATA CAIXA'], dayfirst=True)
    df['DATA COMPETÊNCIA'] = pd.to_datetime(df['DATA COMPETÊNCIA'], dayfirst=True)

    # Selecionar tipo de data para análise
    tipo_data = st.radio("📆 Escolha a data para análise:", ["Data Caixa", "Data Competência"])
    coluna_data = 'DATA CAIXA' if tipo_data == "Data Caixa" else 'DATA COMPETÊNCIA'

    df['Mês/Ano'] = df[coluna_data].dt.strftime('%Y-%m')
    df['Tipo'] = df['VALOR'].apply(lambda x: 'Receita' if x > 0 else 'Gasto')

    # Filtro por mês
    meses_disponiveis = sorted(df['Mês/Ano'].unique(), reverse=True)
    meses_selecionados = st.multiselect("📅 Selecione o(s) mês(es)", meses_disponiveis, default=meses_disponiveis[:1])

    if not meses_selecionados:
        st.warning("Selecione ao menos um mês para visualizar os dados.")
        return

    df_filtrado = df[df['Mês/Ano'].isin(meses_selecionados)]

    # Critério de agrupamento: Categoria ou Conta
    criterio = st.radio("🔍 Analisar gastos por:", ["Categoria", "Conta"])
    coluna_slct = "CATEGORIA" if criterio == "Categoria" else "CONTA"

    # Agrupar receitas e gastos
    df_receitas = df_filtrado[df_filtrado['Tipo'] == 'Receita'].groupby(coluna_slct)['VALOR'].sum().reset_index()
    df_gastos = df_filtrado[df_filtrado['Tipo'] == 'Gasto'].groupby(coluna_slct)['VALOR'].sum().reset_index()

    #aLERT
    df_gastos['VALOR'] = df_gastos['VALOR'].abs()

    # Resumo financeiro
    total_receitas = df_receitas['VALOR'].sum() if not df_receitas.empty else 0
    total_gastos = df_gastos['VALOR'].sum() if not df_gastos.empty else 0
    saldo = total_receitas - total_gastos

    st.subheader(f"Resumo Financeiro - {meses_selecionados}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Receitas", f"R$ {total_receitas:,.2f}")
    col2.metric("Total Gastos", f"R$ {total_gastos:,.2f}")
    col3.metric("Saldo do Mês", f"R$ {saldo:,.2f}", delta=f"R$ {saldo:,.2f}")

    # Cálculo do saldo total acumulado (toda a base)
    total_receitas_geral = df[df['Tipo'] == 'Receita']['VALOR'].sum()
    total_gastos_geral = df[df['Tipo'] == 'Gasto']['VALOR'].abs().sum()
    saldo_total = total_receitas_geral - total_gastos_geral

    st.subheader("🏦 Saldo Acumulado por Conta")

    saldo_contas = df.groupby('CONTA')['VALOR'].sum().reset_index()
    saldo_contas = saldo_contas.sort_values(by='VALOR', ascending=False)

    st.dataframe(saldo_contas, use_container_width=True)

    st.subheader(f"💳 Totais por Conta no(s) mês(es) selecionado(s): {', '.join(meses_selecionados)}")

    totais_contas_mes = df_filtrado.groupby('CONTA')['VALOR'].sum().reset_index()
    totais_contas_mes = totais_contas_mes.sort_values(by='VALOR', ascending=False)

    st.dataframe(totais_contas_mes, use_container_width=True)

    st.subheader("📊 Visão Geral Acumulada")
    col4, col5, col6 = st.columns(3)
    col4.metric("Receitas Totais", f"R$ {total_receitas_geral:,.2f}")
    col5.metric("Gastos Totais", f"R$ {total_gastos_geral:,.2f}")
    col6.metric("Saldo Geral", f"R$ {saldo_total:,.2f}")

    # Tabelas com Top 5
    st.subheader("🏆 Top 5 com Maior Receita")
    if not df_receitas.empty:
        st.write(df_receitas.sort_values(by="VALOR", ascending=False).head(5))
    else:
        st.write("Nenhuma receita encontrada para este mês.")

    st.subheader("💰 Top 5 com Maior Gasto")
    if not df_gastos.empty:
        st.write(df_gastos.sort_values(by="VALOR", ascending=False).head(5))
    else:
        st.write("Nenhum gasto encontrado para este mês.")

    # Gráficos
    if not df_receitas.empty:
        fig_receitas = px.bar(df_receitas, x=coluna_slct, y='VALOR', color=coluna_slct,
                              title=f'Receitas por {criterio} - {meses_selecionados}',
                              labels={'VALOR': 'Valor (R$)', coluna_slct: criterio})
        st.plotly_chart(fig_receitas)
    else:
        st.write("Nenhuma receita encontrada para este mês.")

    if not df_gastos.empty:
        fig_gastos = px.bar(df_gastos, x=coluna_slct, y='VALOR', color=coluna_slct,
                            title=f'Gastos por {criterio} - {meses_selecionados}',
                            labels={'VALOR': 'Valor (R$)', coluna_slct: criterio})
        st.plotly_chart(fig_gastos)
    else:
        st.write("Nenhum gasto encontrado para este mês.")

    # Análise por subcategoria
    st.header("🔎 Análise por Subcategoria")

    Dados = perfil.Dados()
    categorias_disponiveis = Dados.get_categorias_values()
    categoria_analisada = st.selectbox("📂 Escolha uma categoria para ver detalhes das subcategorias", ["Nenhuma"] + list(categorias_disponiveis))

    if categoria_analisada != "Nenhuma":
        df_sub = df_filtrado[df_filtrado['CATEGORIA'] == categoria_analisada] 
        
        df_receitas_sub = df_sub[df_sub['Tipo'] == 'Receita'].groupby('SUBCATEGORIA')['VALOR'].sum().reset_index()
        df_gastos_sub = df_sub[df_sub['Tipo'] == 'Gasto'].groupby('SUBCATEGORIA')['VALOR'].sum().reset_index()
        df_gastos_sub['VALOR'] = df_gastos_sub['VALOR'].abs()

        df_subcategorias = df_sub.groupby(['SUBCATEGORIA', 'Tipo'])['VALOR'].sum().reset_index()
        if not df_subcategorias.empty:
            fig_subcategorias = px.bar(df_subcategorias, x='SUBCATEGORIA', y='VALOR', color='Tipo', barmode='group',
                                       title=f"📊 Receitas e Gastos por Subcategoria - {categoria_analisada}")
            st.plotly_chart(fig_subcategorias)

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

        # Análise histórica da subcategoria
    st.header("📅 Tendência da Subcategoria ao longo do tempo")

    if categoria_analisada != "Nenhuma":
        subcategorias_disponiveis = df[df['CATEGORIA'] == categoria_analisada]['SUBCATEGORIA'].unique()
        subcategoria_analisada = st.selectbox("📌 Escolha uma subcategoria para ver a tendência", ["Nenhuma"] + sorted(subcategorias_disponiveis))

        if subcategoria_analisada != "Nenhuma":
            # Pega o mês mais recente selecionado
            ultimo_mes = max(meses_selecionados)

            # Converte para datetime
            data_ultima = pd.to_datetime(ultimo_mes + "-01")
            meses_retroativos = [(data_ultima - pd.DateOffset(months=i)).strftime('%Y-%m') for i in range(5, -1, -1)]

            df_sub_hist = df[
                (df['CATEGORIA'] == categoria_analisada) &
                (df['SUBCATEGORIA'] == subcategoria_analisada) &
                (df['Mês/Ano'].isin(meses_retroativos)) &
                (df['Tipo'] == 'Gasto')
            ].groupby('Mês/Ano')['VALOR'].sum().reindex(meses_retroativos, fill_value=0).reset_index()

            df_sub_hist['VALOR'] = df_sub_hist['VALOR'].abs()

            fig_sub_hist = px.bar(df_sub_hist, x='Mês/Ano', y='VALOR',
                                  title=f"📊 Gastos com '{subcategoria_analisada}' nos últimos 6 meses",
                                  labels={'VALOR': 'Valor (R$)', 'Mês/Ano': 'Mês'},
                                  color_discrete_sequence=["#EF553B"])
            st.plotly_chart(fig_sub_hist, use_container_width=True)

    st.button("Voltar", on_click=voltar, key="voltar")

def analise_contas():
    import plotly.express as px
    import streamlit as st
    import pandas as pd
    import perfil

    df = pd.read_csv("database/export.csv")
    df['VALOR'] = pd.to_numeric(df['VALOR'])
    df['DATA CAIXA'] = pd.to_datetime(df['DATA CAIXA'], dayfirst=True)
    df['DATA COMPETÊNCIA'] = pd.to_datetime(df['DATA COMPETÊNCIA'], dayfirst=True)

    # Selecionar tipo de data para análise
    tipo_data = st.radio("📆 Escolha a data para análise:", ["Data Caixa", "Data Competência"])
    coluna_data = 'DATA CAIXA' if tipo_data == "Data Caixa" else 'DATA COMPETÊNCIA'

    df['Mês/Ano'] = df[coluna_data].dt.strftime('%Y-%m')
    df['Tipo'] = df['VALOR'].apply(lambda x: 'Receita' if x > 0 else 'Gasto')

    # Filtro por mês
    meses_disponiveis = sorted(df['Mês/Ano'].unique(), reverse=True)
    meses_selecionados = st.multiselect("📅 Selecione o(s) mês(es)", meses_disponiveis, default=meses_disponiveis[17])

    if not meses_selecionados:
        st.warning("Selecione ao menos um mês para visualizar os dados.")
        return

    df_filtrado = df[df['Mês/Ano'].isin(meses_selecionados)]

    # 💳 Faturas de Cartões de Crédito no(s) mês(es) selecionado(s)
    st.subheader("💳 Faturas de Cartões de Crédito no(s) mês(es) selecionado(s)")

    # Filtrar apenas as contas que começam com "CC" (Cartão de Crédito)
    df_cartoes = df_filtrado[
        (df_filtrado['CONTA'].str.startswith("CC"))
    ]

    # Agrupar por conta e somar os gastos
    faturas_cartoes = df_cartoes.groupby('CONTA')['VALOR'].sum().abs().reset_index()
    faturas_cartoes.columns = ['Cartão', 'Total da Fatura']

    # Exibir como tabela
    if not faturas_cartoes.empty:
        st.dataframe(faturas_cartoes.sort_values(by='Total da Fatura', ascending=False), use_container_width=True)
    else:
        st.write("Nenhuma fatura de cartão encontrada para o(s) mês(es) selecionado(s).")

    # Cartões disponíveis no mês filtrado
    cartoes_disponiveis = faturas_cartoes['Cartão'].unique()

    cartao_selecionado = st.selectbox(
        "📌 Selecione um cartão para visualizar faturas", 
        options=["Nenhum"] + list(cartoes_disponiveis)
    )

    if cartao_selecionado != "Nenhum":
        # Pega o último mês selecionado
        ultimo_mes = max(meses_selecionados)

        # Transforma em datetime
        data_base = pd.to_datetime(ultimo_mes + "-01")

        # Gera a lista de 7 meses: 3 anteriores, o atual e 3 posteriores
        meses_analise = [(data_base + pd.DateOffset(months=i)).strftime('%Y-%m') for i in range(-3, 4)]

        # Filtrar os dados do cartão para esses meses
        df_cartao_periodo = df[
            (df['CONTA'] == cartao_selecionado) &
            (df['Mês/Ano'].isin(meses_analise))
        ].groupby('Mês/Ano')['VALOR'].sum().abs().reindex(meses_analise, fill_value=0).reset_index()

        df_cartao_periodo.columns = ['Mês/Ano', 'Fatura']

        # Exibir gráfico
        fig = px.bar(df_cartao_periodo, x='Mês/Ano', y='Fatura',
             title=f"📈 Evolução das Faturas - {cartao_selecionado}",
             labels={'Fatura': 'Valor (R$)', 'Mês/Ano': 'Mês'},
             color_discrete_sequence=["#636EFA"],
             text='Fatura')  # <- adiciona o texto no gráfico
        fig.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')  # <- formatação dos valores
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"📊 Detalhamento por Categoria - {cartao_selecionado} ({ultimo_mes})")
        # Filtrar apenas o mês base (o último mês selecionado)
        df_cartao_mes = df[
            (df['CONTA'] == cartao_selecionado) &
            (df['Mês/Ano'] == ultimo_mes)
        ]

        if not df_cartao_mes.empty:
            # Criar coluna "Tipo Cartão" para identificar gasto ou estorno
            df_cartao_mes['Tipo Cartão'] = df_cartao_mes['VALOR'].apply(lambda x: 'Gasto' if x < 0 else 'Estorno')
            df_cartao_mes['VALOR_ABS'] = df_cartao_mes['VALOR'].abs()

            # Agrupar por categoria e tipo (gasto ou estorno)
            df_cat_tipo = df_cartao_mes.groupby(['CATEGORIA', 'Tipo Cartão'])['VALOR_ABS'].sum().reset_index()

            # Gráfico de barras agrupadas
            fig_cat = px.bar(
                df_cat_tipo,
                x='CATEGORIA',
                y='VALOR_ABS',
                color='Tipo Cartão',
                barmode='group',
                title=f"🧾 Gastos e Estornos por Categoria - {ultimo_mes}",
                labels={'VALOR_ABS': 'Valor (R$)', 'CATEGORIA': 'Categoria'},
                text='VALOR_ABS'
            )
            fig_cat.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside', textfont_size=50)
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.write("Nenhum gasto ou estorno encontrado para esse cartão no mês selecionado.")

    st.button("Voltar", on_click=voltar, key="voltar")




    



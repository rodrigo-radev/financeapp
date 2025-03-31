import json, os, csv
import streamlit as st
import matplotlib.pyplot as plt
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
    from skttest4 import classificacao
    for i in itens.get_all():
        classificacao(i)
    try:
        to_csv(itens.to_dict(),"./database/classificado.csv", True)
    except Exception as e:
        st.write(e)
        df = itens.to_json()
        df = pd.read_json(df)
        st.write(df)

def exibir_graficos():
    st.title("Gráficos")
    st.write("Aqui você pode visualizar gráficos da base de dados.")
    import perfil

    auto = perfil.Itens()
    auto.from_csv("./database/export.csv")
    manual = perfil.Itens()
    manual.from_csv("./database/entrada_manual.csv")

    unificado = unificar(auto, manual)
    
    # Converter para DataFrame
    df = pd.DataFrame(unificado.to_dict())

    # Converter a coluna VALOR para float, tratando valores inválidos
    df["VALOR"] = pd.to_numeric(df["VALOR"], errors='coerce')

    # Soma apenas os valores negativos
    soma_negativos = df[df["VALOR"] < 0]["VALOR"].sum()
    st.write(f"Soma dos valores negativos: {soma_negativos}")

    # Soma apenas os valores positivos
    soma_positivos = df[df["VALOR"] > 0]["VALOR"].sum()
    st.write(f"Soma dos valores positivos: {soma_positivos}")
    
    st.write(f"SOMA TOTAL: {soma_negativos + soma_positivos}")

    # Filtrar valores maiores que 1000 e menores que -1000
    df_extremos = df[(df["VALOR"] > 10000) | (df["VALOR"] < -10000)]
    grouped_extremos_positivos = df_extremos[df_extremos["VALOR"] > 0].groupby("POTE")["VALOR"].sum().reset_index()
    grouped_extremos_negativos = df_extremos[df_extremos["VALOR"] < 0].groupby("POTE")["VALOR"].sum().reset_index()

    # Filtrar valores entre -1000 e 1000
    df_intermediarios = df[(df["VALOR"] >= -10000) & (df["VALOR"] <= 10000)]
    grouped_intermediarios_positivos = df_intermediarios[df_intermediarios["VALOR"] > 0].groupby("POTE")["VALOR"].sum().reset_index()
    grouped_intermediarios_negativos = df_intermediarios[df_intermediarios["VALOR"] < 0].groupby("POTE")["VALOR"].sum().reset_index()

    # Gráfico para valores extremos positivos
    fig1, ax1 = plt.subplots()
    ax1.bar(grouped_extremos_positivos["POTE"], grouped_extremos_positivos["VALOR"], color="green")
    ax1.set_title("Soma dos Valores Positivos por POTE (Extremos: >1000)")
    ax1.set_xlabel("POTE")
    ax1.set_ylabel("Soma dos Valores")
    plt.xticks(rotation=90)
    st.pyplot(fig1)

    # Gráfico para valores extremos negativos
    fig2, ax2 = plt.subplots()
    ax2.bar(grouped_extremos_negativos["POTE"], grouped_extremos_negativos["VALOR"], color="red")
    ax2.set_title("Soma dos Valores Negativos por POTE (Extremos: <-1000)")
    ax2.set_xlabel("POTE")
    ax2.set_ylabel("Soma dos Valores")
    plt.xticks(rotation=90)
    st.pyplot(fig2)

    # Gráfico para valores intermediários positivos
    fig3, ax3 = plt.subplots()
    ax3.bar(grouped_intermediarios_positivos["POTE"], grouped_intermediarios_positivos["VALOR"], color="blue")
    ax3.set_title("Soma dos Valores Positivos por POTE (Intermediários: -1000 a 1000)")
    ax3.set_xlabel("POTE")
    ax3.set_ylabel("Soma dos Valores")
    plt.xticks(rotation=90)
    st.pyplot(fig3)

    # Gráfico para valores intermediários negativos
    fig4, ax4 = plt.subplots()
    ax4.bar(grouped_intermediarios_negativos["POTE"], grouped_intermediarios_negativos["VALOR"], color="orange")
    ax4.set_title("Soma dos Valores Negativos por POTE (Intermediários: -1000 a 1000)")
    ax4.set_xlabel("POTE")
    ax4.set_ylabel("Soma dos Valores")
    plt.xticks(rotation=90)
    st.pyplot(fig4)

    st.button("Voltar", on_click=voltar, key="voltar")
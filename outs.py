import json, os, csv
import streamlit as st
import treat as t
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

def to_csv(itens, file_path):
    """
    Escreve os dados de uma lista de dicionários em um arquivo CSV.
    :param itens: Lista de dicionários contendo os dados a serem salvos.
    :param file_path: Caminho do arquivo CSV onde os dados serão salvos.
    """
    if not itens:
        print("A lista de itens está vazia. Nenhum dado será salvo.")
        return

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

def unificar_json():
    os.remove("./database/unificado.json") if os.path.exists("./database/unificado.json") else None
    arquivo_saida = "./database/unificado.json"
    diretorio = "./database"
    dados_unificados = {"gastos": []}

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".json"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            dados = t.get_json(caminho_arquivo)
            dados_unificados["gastos"].extend(dados["gastos"])

    salva_json(arquivo_saida, dados_unificados)

def exibir_graficos():
    # Carregar dados unificados
    dados = t.get_json("./database/unificado.json")

    # Converter dados para DataFrame
    df = pd.DataFrame(dados["gastos"])

    # Converter coluna de data para datetime
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")

    # Substituir valores vazios por NaN e remover linhas com valores inválidos
    df["valor"] = df["valor"].replace({'R\$ ': '', '.': '', ',': '.'}, regex=True).replace('', pd.NA).dropna()

    # Converter coluna de valor para numérico
    df["valor"] = df["valor"].astype(float)

    # Remover linhas com datas inválidas
    df = df.dropna(subset=["data"])

    # Plotar gráfico de gastos ao longo do tempo
    plt.figure(figsize=(12, 8))
    plt.plot(df["data"], df["valor"], marker='o')
    plt.xlabel("Data")
    plt.xlim(df["data"].min(), df["data"].max())
    plt.ylabel("Valor (R$)")
    plt.title("Gastos ao longo do tempo")
    plt.grid(True)
    st.pyplot(plt)

def exibir_database():
    st.title("Database Completa")
    unificar_json()
    st.write(t.get_json("./database/unificado.json"))

    st.button("Voltar", on_click=voltar,key="voltar")
    
    if st.button("Exibir graficos"):
        exibir_graficos()
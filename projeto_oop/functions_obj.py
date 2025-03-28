import streamlit as st
import pdfplumber, os
import json, os
import matplotlib.pyplot as plt
import pandas as pd
import openai
from datetime import datetime

class functions_obj:
    def __init__(self):
        self.client = openai.OpenAI(api_key='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')
        entry = self.entry()
        outs = self.outs()
        treat = self.treat()

class entry:
    def read_pdf(uploaded_file):
        pdf_text = ""
        file_name = uploaded_file.name
        try:
            if uploaded_file is not None:
                st.write("Arquivo carregado com sucesso!")

                # Lendo o PDF
                try:
                    with pdfplumber.open(uploaded_file) as pdf:
                        pdf_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                except Exception as e:
                    st.write(f"Erro ao ler o arquivo. Tente novamente.\n{e}")
        except Exception as e:
            st.write(f"Erro ao carregar o arquivo. Tente novamente.\n{e}")

        # Retorna o texto extraído do PDF e o nome do arquivo
        return pdf_text, file_name

    def upload_pdf():
        st.title("Carregar PDF")
        uploaded_file = st.file_uploader("Envie um arquivo PDF", type="pdf")

        if uploaded_file is not None:
            pdf_text, file_name = read_pdf(uploaded_file)
            st.session_state['pdf_text'] = pdf_text
            st.session_state['file_name'] = file_name

        if 'pdf_text' in st.session_state:
            pdf_text = st.session_state['pdf_text']
            file_name = st.session_state['file_name']

            #Remove extensão de arquivo .pdf
            file_name = file_name.replace(".pdf","")

            if st.button("Gerar JSON"):
                with st.spinner("Gerando..."):
                    json_file_path = f"./database/{file_name}.json"
                    if os.path.exists(json_file_path):
                        st.warning(f"O arquivo {file_name}.json já existe e não será salvo novamente.")

                        result = t.ler_json(json_file_path)
                        st.session_state['result'] = result
                    else:
                        result = t.to_data(pdf_text)
                        t.tratar_data(result)
                        o.salva_json(json_file_path,result)
                        st.session_state['result'] = result

        if 'result' in st.session_state:
            result = st.session_state['result']
            # Exibir resultado formatado
            st.json(result)

            if st.button("Analisar Extrato"):
                with st.spinner("Analisando..."):
                    # Processar resposta da OpenAI
                    analise = t.analise_extrato(result)
                    st.session_state['analise'] = analise

        if 'analise' in st.session_state:
            analise = st.session_state['analise']
            # Exibir resultado formatado
            st.write(analise)

        st.button("Voltar", on_click=t.voltar,key="voltar")

    def manual_entry():
        st.title("Entrada Manual")

        data = st.date_input("Data")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", value=0.0, step=1.0, format="%.2f",min_value=0.0)

        coluna1, coluna2 = st.columns(2)

        with coluna1:
            if st.button("Adicionar"):
                if 'gastos' not in st.session_state:
                    st.session_state['gastos'] = []

                st.session_state['gastos'].append({
                    "data": data.strftime("%d/%m/%Y"),
                    "descrição": descricao,
                    "valor": valor
                })

                st.success("Gasto adicionado com sucesso!")

            if 'gastos' in st.session_state:
                st.write("Gastos adicionados:")
                st.json(st.session_state['gastos'])

        with coluna2:
            if st.button("Salvar"):
                json_file_path = "./database/manual_entry.json"
                o.salva_json(json_file_path, {"gastos": st.session_state['gastos']})
                st.success(f"Gastos salvos em {json_file_path}")

        st.button("Voltar", on_click=o.voltar,key="voltar")

class outs:
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

class treat():
    def to_data(pdf_text):
        prompt = f"""
            Extraia e formate os dados do seguinte extrato bancário, verificando todo o arquivo para obter transações:
            {pdf_text}
            Retorne os gastos no seguinte formato JSON:
            {{
                "gastos": [
                    {{"data": "DD/MM/YYYY", "descrição": "Descrição da transação", "valor": "XXXX.XX"}},
                    {{"data": "DD/MM/YYYY", "descrição": "Descrição da transação", "valor": "XXXX.XX"}}
                ]
            }}
            """
        response = None  # Inicializa a variável response
        try:  
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a pdf to json converter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            result = response.choices[0].message.content
            return json.loads(result)

        except Exception as e:
            st.write(f"Erro ao processar a requisição. Tente novamente.\n{e}")
            return None

    def tratar_data(result):
        result["gastos"] = [gasto for gasto in result["gastos"] if gasto["data"] and gasto["descrição"] and gasto["valor"]]
        for gasto in result["gastos"]:
            #A data vem no formato DD/MM/YYYY, então é necessário converter para o formato datetime
            data_atual = datetime.now()
            dia, mes, ano = gasto["data"].split("/")
            mes = int(mes)

            if int(mes) < data_atual.month:
                ano = data_atual.year
            else:
                ano = data_atual.year - 1

            gasto["data"] = f"{dia}/{mes}/{ano}"

            #Transformar valor em float
            gasto["valor"] = float(gasto["valor"].replace('.','').replace(',', '.'))

    def analise_extrato(database):
        prompt = f"""
            Leia os dados do seguinte banco de dados:
            {database}
            "data" significa o dia do mês em que a transação ocorreu.
            "descrição" é o nome da transação, coloque os semelhantes numa mesma categoria sempre que possivel.
            "valor" é o valor da transação.
            se houver algo como uma data XX/YY na descrição considere como um parcelamento.
            Quero saber:
            o dia da semana que mais foi gasto dinheiro, use o calendario para descobrir.
            baseado no baixo valor, quais itens poderiam ter sido evitados. Nada parcelado poderia ter sido evitado.
            Quanto eu gastei com parcelamentos.
            """

        response = None  # Inicializa a variável response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )
            result = response.choices[0].message.content
            return result

        except Exception as e:
            st.write(f"Erro ao processar a requisição. Tente novamente.\n{e}")
            return None
        
    def ler_json(json_file_path):
        try:
            with open(json_file_path, "r") as json_file:
                result = json.load(json_file)
                return result
        except Exception as e:
            st.write(f"Erro ao ler o arquivo JSON. Tente novamente.\n{e}")

    def get_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
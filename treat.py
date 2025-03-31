import openai, json
import streamlit as st
from datetime import datetime

client = openai.OpenAI(api_key='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')

def to_data(pdf_text):

    lista = pdf_text.split("\n")
    for linha in lista:
        if "Lançamentos: compras e saques" in linha:
            #exclui tudo que vem antes de Lançamentos
            lista = lista[lista.index(linha):]
            break
    for linha in lista:
        if "Fique atento aos encargos para o próximo" in linha:
            #exclui tudo que vem depois de Fique atento
            lista = lista[:lista.index(linha)]
            break
    pdf_text = "\n".join(lista)

    prompt = f"""
        Extraia e formate todos os dados do seguinte extrato bancário, que está em formato de texto:
        {pdf_text}
        Devem haver quase 80 transações.
        Retorne os gastos no seguinte formato de dict:
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
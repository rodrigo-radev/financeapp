import streamlit as st
import pdfplumber, os
import treat as t
import outs as o
from item import item
from datetime import datetime
import json

def read_pdf(uploaded_file):
    pdf_text = ""
    file_name = uploaded_file.name
    try:
        if uploaded_file is not None:
            st.write("Arquivo carregado com sucesso!")

            # Lendo o PDF
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        pdf_text += text
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
                    
                    #salvar result em arquivo
                    with open(json_file_path, "w") as json_file:
                        json.dump(result, json_file)
                    #t.tratar_data(result)
                    #o.salva_json(json_file_path,result)
                    st.session_state['result'] = result

    if 'result' in st.session_state:
        result = st.session_state['result']
        # Exibir resultado formatado
        st.json(result)
        st.write(result)

    st.button("Voltar", on_click=o.voltar,key="voltar")

def manual_entry():
    st.title("Entrada Manual")

    #Dados para entrada manual
    lancamento = item()
    
    arquivo_categorias = json.loads(open("categorias.json").read())
    contas_correntes = ["ITAÚ","BRADESCO","BB","C6","Neon","Nubank"]
    cartoes_credito = {"CC Nubank":1,"CC Bradesco":5,"CC Itaú Black":17,"CC Itaú Master":6,"CC MercadoPago":7,"CC SAMS":1}
    complemento = ""


    lancamento.date = st.date_input("Data de competência",format="DD/MM/YYYY")

    colmn1,colmn2 = st.columns(2)
    with colmn1:
        ehcartao = st.checkbox("É cartão de crédito?",value=True)
    
    if (ehcartao):
        lancamento.account = st.selectbox("Conta", cartoes_credito)

        if lancamento.date.day < cartoes_credito[lancamento.account]:
            datames = lancamento.date.month
        else:
            datames = lancamento.date.month+1
        
        lancamento.date_payment = datetime(lancamento.date.year,
                                           datames,
                                           cartoes_credito[lancamento.account]) 

        with colmn2:
            ehparcelado = st.checkbox("É parcelado?")
        if ehparcelado:
            c1,c2 = st.columns(2)
            with c1:
                lancamento.parcelas = st.number_input("Número de parcelas", value=1, step=1, min_value=1)
            with c2:
                lancamento.n_parcelas = st.number_input("Qual parcela", value=1, step=1, min_value=1, max_value=lancamento.parcelas)
                complemento += f" {lancamento.n_parcelas}/{lancamento.parcelas}"
    else: 
        lancamento.date_payment = st.date_input("Data de caixa",format="DD/MM/YYYY")
        lancamento.account = st.selectbox("Conta", contas_correntes)

    lancamento.date = lancamento.date.strftime("%d/%m/%Y")
    lancamento.date_payment = lancamento.date_payment.strftime("%d/%m/%Y")

    lancamento.name = st.text_input("Descrição") + complemento
    
    lancamento.price = st.number_input("Valor", value=0.0, step=1.0, format="%.2f")

    col1,col2,col3 = st.columns(3)
    with col1:
        lancamento.type = st.selectbox("POTE",arquivo_categorias.keys())
    with col2:
        lancamento.category = st.selectbox("Categoria",arquivo_categorias[lancamento.type])
    with col3:
        lancamento.subcategory = st.selectbox("Subcategoria",arquivo_categorias[lancamento.type][lancamento.category])

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        if st.button("Adicionar"):
            if 'gastos' not in st.session_state:
                st.session_state['gastos'] = []

            st.session_state['gastos'].append(lancamento.to_dict())

            st.success("Gasto adicionado com sucesso!")

        if 'gastos' in st.session_state:
            st.write("Gastos adicionados:")
            st.json(st.session_state['gastos'])

    with coluna2:
        if st.button("Salvar"):
            json_file_path = "./database/entrada_manual.csv"
            o.to_csv({"gastos": st.session_state['gastos']},json_file_path)
            st.success(f"Gastos salvos em {json_file_path}")

    st.button("Voltar", on_click=o.voltar,key="voltar")
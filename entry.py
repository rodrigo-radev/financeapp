import streamlit as st
import outs as o
import perfil as pf
import bancos as bc
from datetime import datetime
dados = pf.Dados()

def upload_pdf(conta):
    st.title("Upload PDF")
    upload_pdf = st.file_uploader("ENVIE UM ARQUIVO PDF", type='pdf')
    
    if upload_pdf is not None:
        if conta == 'Itau':
            lancamentos = bc.Itau.pdfread(upload_pdf)
        elif conta == 'Bradesco':
            st.warning(bc.Banco_generico.output())
        elif conta == 'MercadoPago':
            st.warning(bc.Banco_generico.output())
        else:
            st.warning(bc.Banco_generico.output())
            
    st.button("Voltar", on_click=o.voltar,key="voltar")
    
def upload_csv(conta):
    st.title("Upload CSV")
    upload_csv = st.file_uploader("ENVIE UM ARQUIVO EM FORMATO CSV", type="csv")

    if upload_csv is not None:
        if conta == 'Itau':
            lancamentos = bc.Itau.csvread(upload_csv)
            item = pf.Item()
            for i in lancamentos:
                item.set_account(conta)
                item.set_date(i['Data'])
        elif conta == 'Bradesco':
            st.warning(bc.Banco_generico.output())
        elif conta == 'MercadoPago':
            st.warning(bc.Banco_generico.output())
        elif conta == 'NovoBanco':
            lancamentos = bc.NovoBanco.csvread(upload_csv)
        else:
            st.warning(bc.Banco_generico.output())
    
    st.button("Voltar", on_click=o.voltar,key="voltar")

def upload_xls(conta):
    st.title("Upload arquivo tipo Excel")
    upload_xls = st.file_uploader("ENVIE UM ARQUIVO DO TIPO .XLS,XLSX",type=['xls','xlsx'])
    processado = False

    if upload_xls is not None:
        if conta == 'Itau':
            lancamentos = bc.Itau.xlsread(upload_xls)
            lancamento = pf.Itens()
            processado = lancamento.add_lancamento(lancamentos,conta)
        elif conta == "NovoBanco":
            lancamentos = bc.NovoBanco.xlsread(upload_xls)
            lancamento = pf.Itens()
            processado = lancamento.add_lancamento(lancamentos,conta)
        elif conta == 'BRADESCO':
            st.warning(bc.Banco_generico.output())
        elif conta == 'CC MercadoPago':
            st.warning(bc.Banco_generico.output())
        else:
            st.warning(bc.Banco_generico.output())

    if processado:          
        if st.button("Salvar"):
            json_file_path = "./database/auto.csv"
            o.to_csv(lancamento,json_file_path)
            
            #Após salvar limpar a lista de gastos
            lancamento.reset()
            st.success(f"Gastos salvos em {json_file_path}")

    st.button("Voltar", on_click=o.voltar,key="voltar")

def manual_entry():
    st.title("Entrada Manual")

    #Dados para entrada manual
    lancamento = pf.Item()
    perfil = pf.Dados()
    
    arquivo_categorias = perfil.get_categorias()
    contas_correntes = perfil.get_contas()
    cartoes_credito = perfil.get_cartoes()
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

    coluna1, coluna2, coluna3 = st.columns(3)

    with coluna1:
        if st.button("Adicionar"):
            if 'gastos' not in st.session_state:
                st.session_state['gastos'] = []

            adicionado = lancamento.to_dict()
            if(adicionado in st.session_state['gastos']):
                st.warning("Gasto já adicionado/repetido")
            else:
                st.session_state['gastos'].append(adicionado)
                st.success("Gasto adicionado com sucesso!")

        if 'gastos' in st.session_state:
            st.write("Gastos adicionados:")
            st.json(st.session_state['gastos'])

    with coluna2:
        if st.button("Salvar"):
            json_file_path = "./database/entrada_manual.csv"
            o.to_csv(st.session_state['gastos'],json_file_path)
            
            #Após salvar limpar a lista de gastos
            st.session_state['gastos'] = []
            st.success(f"Gastos salvos em {json_file_path}")

    with coluna3:
        if st.button("Exportar",key='exportar'):
            file = './database/entrada_manual.csv'
            import pandas as pd
            expo = pd.read_csv(file)
            expo.to_excel('database/novoexport.xlsx')
            st.success("Arquivo exportado")

    st.button("Voltar", on_click=o.voltar,key="voltar")
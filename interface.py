import streamlit as st
import entry as e
import outs as o
import perfil
import skttest4
from streamlit_option_menu import option_menu
perfil = perfil.Dados()
contas = list(perfil.get_cartoes())
contas.extend(perfil.get_contas())

# Funções para cada página
def home():
    st.title("MVP - Extrato Bancário")
    
    #botões em colunas para escolha de entrada de dados
    col1, col2, col3= st.columns(3)
    with col1:
        if st.button("Carregar PDF"):
            st.session_state.page = "upload_pdf"
        if st.button("Carregar CSV"):
            st.session_state.page = "upload_csv"
        if st.button("Carregar XLS"):
            st.session_state.page = "upload_excel"
    with col2:
        if st.button("Entrada manual"):
            st.session_state.page = "manual_entry"
    with col3:
        if st.button("Exibir gráficos"):
            st.session_state.page = "graficos"
        if st.button("Visualizar base de dados"):
            st.session_state.page = "base de dados"
    
    st.divider()

    st.session_state['Banco'] = st.selectbox('Selecione o banco:',contas,index=6)
    if st.button("Rerun"):
        st.rerun()

# Inicializar a página inicial
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Navegação entre páginas
if st.session_state.page == "home":
    home()

elif st.session_state.page == "upload_pdf":
    e.upload_pdf(st.session_state['Banco'])
elif st.session_state.page == "upload_excel":
    e.upload_xls(st.session_state['Banco'])
elif st.session_state.page == "upload_csv":
    e.upload_csv(st.session_state['Banco'])

elif st.session_state.page == "manual_entry":
    e.manual_entry()

elif st.session_state.page == "graficos":
    o.exibir_graficos()
elif st.session_state.page == "base de dados":
    o.exibir_database()   
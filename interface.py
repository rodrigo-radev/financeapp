import streamlit as st
import entry as e
import outs as o
from streamlit_option_menu import option_menu

# Funções para cada página
def home():
    st.title("MVP - Extrato Bancário")
    
    #botões em colunas para escolha de entrada de dados
    col1, col2, col3= st.columns(3)
    with col1:
        if st.button("Carregar PDF"):
            st.session_state.page = "upload_pdf"
    with col2:
        if st.button("Entrada manual"):
            st.session_state.page = "manual_entry"
    with col3:
        if st.button("Exibir database completa"):
            st.session_state.page = "database"
    
    if st.button("Rerun"):
        st.rerun()

# Inicializar a página inicial
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Navegação entre páginas
if st.session_state.page == "home":
    home()
elif st.session_state.page == "upload_pdf":
    e.upload_pdf()
elif st.session_state.page == "manual_entry":
    e.manual_entry()
elif st.session_state.page == "database":
    o.exibir_database()
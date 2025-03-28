from functions_obj import entry, treat, outs
import streamlit as st

class Interface:
    def __init__(self):
        self.page = "home"
    
    def home(self):
        st.title("MVP - Extrato Bancário")
        
        #botões em colunas para escolha de entrada de dados
        col1, col2, col3= st.columns(3)
        with col1:
            if st.button("Carregar PDF"):
                self.page = "upload_pdf"
        with col2:
            if st.button("Entrada manual"):
                self.page = "manual_entry"
        with col3:
            if st.button("Exibir database completa"):
                self.page = "database"
        
        if st.button("Rerun"):
            st.rerun()

    def run(self):
        # Navegação entre páginas
        if self.page == "home":
            self.home()
        elif self.page == "upload_pdf":
            entry.upload_pdf()
        elif self.page == "manual_entry":
            entry.manual_entry()
        elif self.page == "database":
            outs.exibir_database()
#Transformar tudo em um dicionario apenas
dicionario_rafael = {
    "Despesas Básicas": {
        "Alimentação": ["Mercado", "Restaurante", "Lanches", "Padaria", "Suplementação"],
        "Assinaturas": ["Telefone", "Fotos", "Stream"],
        "Transporte": ["Aplicativo", "Carro manutenção", "Carro melhorias", "Estacionamento", "Combustível"],
        "Casa": ["Diarista Alimentação", "Diarista Limpeza", "Água e Luz", "Jardineiro", "Manutenção Casa", "Material de limpeza"],
        "Cuidado pessoal": ["Academia", "Cabeleireiro", "Estética", "Saúde"],
        "Vestuário": ["Roupas", "Calçados", "Acessórios"],
        "Seguro": ["Carro", "Vida", "Residencial"],
        "Esporte": ["Academia", "Equipamento"],
        "Férias": ["Passagem", "Hospedagem", "Alimentação", "Passeios"]
    },
    "Despesas Profissionais": {
        "Taxa": ["Banco", "Plataforma"],
        "Gestor": ["Gestão"],
        "Estagiario": ["Estágio"],
        "Projetos": ["Projeto1", "Projeto2", "Projeto3"]
    },
    "Doação": {
        "Presentes": ["Aniversário", "Natal"],
        "UDV": ["Dízimo"]
    },
    "Investimento": {
        "Bens Materias": ["Equipamento"],
        "Férias": ["Passagem", "Hospedagem", "Alimentação", "Passeios"],
        "Casa": ["Aluguel", "Condomínio", "Água", "Luz", "Gás", "Telefone", "Internet"],
        "Kite": ["Material"],
        "Escritório": ["Material"]
    },
    "Emprestimos": {
        "Bloqueio Judicial": ["Bloqueio Judicial"], 
        "Financeamento":["Financeamento"], 
        "Juros":["Juros"], 
        "Fundo Abreu":["Fundo Abreu"], 
        "Ingrid":["Ingrid"], 
        "Terceiros":["Terceiros"], 
        "Encontro de contas":["Encontro de contas"], 
        "Saque":["Saque"]
    }
}
import json
dicionario_rafael_json = json.dumps(dicionario_rafael, indent=4, ensure_ascii=True)

#salvar em arquivo
with open("categorias.json", "w") as f:
    f.write(dicionario_rafael_json)
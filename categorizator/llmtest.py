import pandas as pd

caminho_csv = r"C:\Users\Normando\Desktop\pyprojects\projeto02\dados_tratados.csv"

df = pd.read_csv(caminho_csv)

print(df.columns)

df = df.drop(['NATUREZA', 'AUTOMÁTICO', 'PARCELAS', 'N PARCELA'], axis=1)

print(df.columns)

def consulta(descricao, df):
    transacoes_similares = df[df['DESCRIÇÃO'].str.contains(descricao, case=False, na=False)]
    
    if not transacoes_similares.empty:
        return transacoes_similares[['DESCRIÇÃO', 'CONTA', 'POTE', 'CATEGORIA', 'SUBCATEGORIA']].head(5)
    else:
        return "Nenhuma transação similar encontrada"


from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

prompt_template = """
Dado o lançamento financeiro com a seguinte informação:
Descrição: {descricao}

Transações similares encontradas no histórico:
{historico_transacoes}

Com base nas informações acima, qual seria o pote, categoria e subcategoria para este lançamento?
"""

prompt = PromptTemplate(input_variables=["descricao", "historico_transacoes"], template=prompt_template)

llm = OpenAI(temperature=0.7, openai_api_key = "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")

chain = LLMChain(prompt=prompt, llm=llm)

def classificar_lançamento(descricao, df):
    historico_transacoes = consulta(descricao, df)
    resposta = chain.run({
            "descricao": descricao,
            "historico_transacoes": historico_transacoes
        })
        
    return resposta

print(classificar_lançamento("levu drinks", df))
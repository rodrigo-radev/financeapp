import pandas as pd
import nltk 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

caminho_csv = "./dadosv3.csv"

df = pd.read_csv(caminho_csv, delimiter=';')

df = df.dropna(subset=['DESCRIÇÃO', 'POTE', 'CATEGORIA', 'SUBCATEGORIA'])

label_encoder_pote = LabelEncoder()
df['POTE'] = label_encoder_pote.fit_transform(df['POTE'])

label_encoder_categoria = LabelEncoder()
df['CATEGORIA'] = label_encoder_categoria.fit_transform(df['CATEGORIA'])

label_encoder_subcategoria = LabelEncoder()
df['SUBCATEGORIA'] = label_encoder_subcategoria.fit_transform(df['SUBCATEGORIA'])

#vetorizacao

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

# Baixar as stopwords em português
nltk.download('stopwords')
from nltk.corpus import stopwords

# Obter as stopwords em português
stop_words = stopwords.words('portuguese')

# Criar o TfidfVectorizer com stopwords em português
tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)

# Ajustar e transformar os dados
X = tfidf_vectorizer.fit_transform(df['DESCRIÇÃO'])

y_pote = df['POTE']
y_categoria = df['CATEGORIA']
y_subcategoria = df['SUBCATEGORIA']

#treino e teste refeitos
X_train, X_test, y_train, y_test = train_test_split(X, df[['POTE', 'CATEGORIA', 'SUBCATEGORIA']], test_size=0.3, random_state=42)

y_train_pote = y_train['POTE']
y_train_categoria = y_train['CATEGORIA']
y_train_subcategoria = y_train['SUBCATEGORIA']

y_test_pote = y_test['POTE']
y_test_categoria = y_test['CATEGORIA']
y_test_subcategoria = y_test['SUBCATEGORIA']

#treinamento do modelo
clf_pote = RandomForestClassifier(n_estimators=100, random_state=42)
clf_pote.fit(X_train, y_train_pote)

clf_categoria = RandomForestClassifier(n_estimators=100, random_state=42)
clf_categoria.fit(X_train, y_train_categoria)

clf_subcategoria = RandomForestClassifier(n_estimators=100, random_state=42)
clf_subcategoria.fit(X_train, y_train_subcategoria)

#avaliacao
y_pred_pote = clf_pote.predict(X_test)
print("Avaliação Pote: ")
print(classification_report(y_test_pote, y_pred_pote))

y_pred_categoria = clf_categoria.predict(X_test)
print("Avaliação Categoria: ")
print(classification_report(y_test_categoria, y_pred_categoria))

y_pred_subcategoria = clf_subcategoria.predict(X_test)
print("Avaliação Subcategoria: ")
print(classification_report(y_test_subcategoria, y_pred_subcategoria))

#Realiza a classificação
def classificacao(descricao):
    descricao_tfidf = tfidf_vectorizer.transform([descricao])

    pote_pred = label_encoder_pote.inverse_transform(clf_pote.predict(descricao_tfidf))
    categoria_pred = label_encoder_categoria.inverse_transform(clf_categoria.predict(descricao_tfidf))
    subcategoria_pred = label_encoder_subcategoria.inverse_transform(clf_subcategoria.predict(descricao_tfidf))

    return pote_pred[0], categoria_pred[0], subcategoria_pred[0]

#é necessario??
def apply_classifier(descricao):
    pote, categoria, subcategoria = classificacao(descricao)
    return pote, categoria, subcategoria

#cria transacao ja classificada
def add_transacao(data_competencia, data_caixa, valor, descricao, conta):
    pote, categoria, subcategoria = apply_classifier(descricao)

    transacao = pd.DataFrame({
        'DATA COMPETÊNCIA': [data_competencia],
        'DATA CAIXA': [data_caixa],
        'DESCRIÇÃO': [descricao],
        'VALOR': [valor],
        'CONTA': [conta],
        'POTE': [None],  # Coluna POTE vazia
        'CATEGORIA': [None],  # Coluna CATEGORIA vazia
        'SUBCATEGORIA': [None],  # Coluna SUBCATEGORIA vazia
        'OBSERVAÇÃO': [None],  # Coluna OBSERVAÇÃO vazia
    })

    transacao['POTE'] = pote
    transacao['CATEGORIA'] = categoria
    transacao['SUBCATEGORIA'] = subcategoria

    return transacao

#Preenche csv
def preencher_csv_arquivo(caminho_csv):
    df = pd.read_csv(caminho_csv)

    for i, row in df.iterrows():
        pote, categoria, subcategoria = apply_classifier(row['DESCRIÇÃO'])

        df.loc[i, 'POTE'] = pote
        df.loc[i, 'CATEGORIA'] = categoria
        df.loc[i, 'SUBCATEGORIA'] = subcategoria

    df.to_csv("./saida.csv", index=False)
    print("CSV preenchido com sucesso!")
    
def preencher_csv(df):
    for i, row in df.iterrows():
        pote, categoria, subcategoria = apply_classifier(row['DESCRIÇÃO'])

        df.loc[i, 'POTE'] = pote
        df.loc[i, 'CATEGORIA'] = categoria
        df.loc[i, 'SUBCATEGORIA'] = subcategoria

    df.to_csv("./saida2.csv", index=False)
    print("CSV preenchido com sucesso!")


##Testando funções
##Cria uma transação e a classifica automaticamente
print(add_transacao('2025-03-20', '2025-03-20', 100.00, 'PIX HARMONIA LOCACOES', 'ITAU'))

##Recebe um csv e classifica todas as transações
dados = pd.read_csv("./dadosv3.csv", delimiter=';')

dados['DATA CAIXA'] = pd.to_datetime(dados['DATA CAIXA'], errors='coerce')

dados = dados[dados['DATA CAIXA'].dt.year == 2025]

preencher_csv(dados)
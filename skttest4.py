import pandas as pd
import nltk 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import perfil

caminho_csv = "./database/auto.csv"

df = pd.read_csv(caminho_csv, delimiter=';')

#df = df.dropna(subset=['DESCRIÇÃO', 'POTE', 'CATEGORIA', 'SUBCATEGORIA'])
print(df.columns)
print(df.head())
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
def classificacao(item):
 
    descricao_tfidf = tfidf_vectorizer.transform([item.get_name()])

    pote_pred = label_encoder_pote.inverse_transform(clf_pote.predict(descricao_tfidf))
    categoria_pred = label_encoder_categoria.inverse_transform(clf_categoria.predict(descricao_tfidf))
    subcategoria_pred = label_encoder_subcategoria.inverse_transform(clf_subcategoria.predict(descricao_tfidf))

    item.set_type(pote_pred[0])
    item.set_category(categoria_pred[0])
    item.set_subcategory(subcategoria_pred[0])

    return item.get_type(), item.get_category(), item.get_subcategory()

#Preenche csv
def preencher_csv_arquivo(caminho_csv):
    pass
    """
    df = pd.read_csv(caminho_csv)

    for i, row in df.iterrows():
        pote, categoria, subcategoria = classificacao(row['DESCRIÇÃO'])

        df.loc[i, 'POTE'] = pote
        df.loc[i, 'CATEGORIA'] = categoria
        df.loc[i, 'SUBCATEGORIA'] = subcategoria

    df.to_csv("./saida.csv", index=False)
    print("CSV preenchido com sucesso!")
    """
def preencher_csv(df):
    """"
    for i, row in df.iterrows():
        pote, categoria, subcategoria = apply_classifier(row['DESCRIÇÃO'])

        df.loc[i, 'POTE'] = pote
        df.loc[i, 'CATEGORIA'] = categoria
        df.loc[i, 'SUBCATEGORIA'] = subcategoria

    df.to_csv("./saida2.csv", index=False)
    print("CSV preenchido com sucesso!")"
    """
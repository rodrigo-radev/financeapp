import pandas as pd
import nltk 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

caminho_csv = r"C:\Users\Normando\Desktop\pyprojects\projeto02\dados_tratados.csv"

df = pd.read_csv(caminho_csv)

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

#treino e teste
X_train, X_test, y_train_pote, y_test_pote = train_test_split(X, y_pote, test_size=0.3, random_state=42)
X_train, X_test, y_train_categoria, y_test_categoria = train_test_split(X, y_categoria, test_size=0.3, random_state=42)
X_train, X_test, y_train_subcategoria, y_test_subcategoria = train_test_split(X, y_subcategoria, test_size=0.3, random_state=42)

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

#Testando na prática
def classificacao(descricao):
    descricao_tfidf = tfidf_vectorizer.transform([descricao])

    pote_pred = label_encoder_pote.inverse_transform(clf_pote.predict(descricao_tfidf))
    categoria_pred = label_encoder_categoria.inverse_transform(clf_categoria.predict(descricao_tfidf))
    subcategoria_pred = label_encoder_subcategoria.inverse_transform(clf_subcategoria.predict(descricao_tfidf))

    return pote_pred[0], categoria_pred[0], subcategoria_pred[0]

transacao = "Point Center"

pote, categoria, subcategoria = classificacao(transacao)

print(f"Pote: {pote}, Categoria: {categoria}, Subcategoria: {subcategoria}")
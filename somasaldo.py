import pandas as pd

df = pd.read_csv("database/export.csv")
df['VALOR'] = pd.to_numeric(df['VALOR'])
df['DATA CAIXA'] = pd.to_datetime(df['DATA CAIXA'], dayfirst=True)
df['DATA COMPETÊNCIA'] = pd.to_datetime(df['DATA COMPETÊNCIA'], dayfirst=True)

itau_black = df[df['CONTA'] == "CC ITAU BLACK"]
itau_black = itau_black[itau_black['DATA CAIXA'] == pd.to_datetime("17/10/2024", dayfirst=True)]

print(itau_black['VALOR'].sum())

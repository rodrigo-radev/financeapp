import pandas as pd

df = pd.read_csv("database/export.csv")
df['VALOR'] = pd.to_numeric(df['VALOR'])
df['DATA CAIXA'] = pd.to_datetime(df['DATA CAIXA'], dayfirst=True)
df['DATA COMPETÊNCIA'] = pd.to_datetime(df['DATA COMPETÊNCIA'], dayfirst=True)

itau_black = df[df['CONTA'] == "ITAÚ"]

print(itau_black['VALOR'].sum())

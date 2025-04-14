import pandas as pd

df = pd.read_csv("database/export.csv")

somageral = df['VALOR'].sum()
print(somageral)

receitas = df[df['VALOR'] >= 0]
gastos = df[df['VALOR'] < 0]

receitas_sum = receitas['VALOR'].sum()
gastos_sum = gastos['VALOR'].sum()

print(receitas_sum)
print(gastos_sum)
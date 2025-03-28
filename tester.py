import pdfplumber

file = "./pdfs/Fatura_Itau_20250226-102719.pdf"
fullpdf = ""
with pdfplumber.open(file) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        fullpdf += text
#print(fullpdf)
#with open("pdfcru.txt", "w") as f:
#    f.write(fullpdf)
#fullpdf = fullpdf.replace("\n", " ")
lista = fullpdf.split("\n")
for linha in lista:
    if "Lançamentos: compras e saques" in linha:
        #exclui tudo que vem antes de Lançamentos
        lista = lista[lista.index(linha):]
        break
for linha in lista:
    if "Fique atento aos encargos para o próximo" in linha:
        #exclui tudo que vem depois de Fique atento
        lista = lista[:lista.index(linha)]
        break
print(lista)
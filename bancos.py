import pandas as pd
class Banco_generico:
    def __init__(self):
        pass
    def output(self):
        return "Ainda não implementado"
class Itau:
    def xlsread(file_path):
        df = pd.read_excel(
            file_path,
            engine='xlrd',
            sheet_name="Lançamentos",
            skiprows=9,  # Skip
            usecols="A:E",
            header=0 
        )

        # Clean column names
        df.columns = [col.strip().lower() for col in df.columns]
        df.columns = ['data', 'lancamento','ag_origem' ,'valor', 'saldo']

        # Convert date column to datetime
        df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

        # Convert value columns to numeric, handling negatives and commas
        for col in ['valor', 'saldo']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows where value is NaN (empty rows)
        df = df.dropna(how='all', subset=['valor'])

        # Forward fill dates for transactions on the same day
        df['data'] = df['data'].ffill()

        # Sort by date (newest first)
        df = df.sort_values('data', ascending=False)

        # Reset index
        df = df.reset_index(drop=True)

        return df
    
    def csvread(upload_csv):
        df = pd.read_csv(upload_csv)

        return df
    
    def pdfread(upload_pdf):
        pass

class NovoBanco:
    def xlsread(file_path):
        try:
            df = pd.read_excel(
                file_path,
                engine='openpyxl',
                sheet_name="ConsultaSaldosMovimentos",
                skiprows=9,  # Skip
                usecols="A:G",
                header=0)
        except:
            try:
                df = pd.read_excel(
                file_path,
                engine='xlrd',
                sheet_name="ConsultaSaldosMovimentos",
                skiprows=9,  # Skip
                usecols="A:G",
                header=0)
            except Exception as e:
                print("\n\n\n",e,'\n\n\n')
                try:
                    df = pd.read_xml(file_path,encoding='latin1')
                except Exception as f:
                    print("\n",f,"\n\n\n\n\n\n\n")
                    return pd.DataFrame()

        # Clean column names
        df.columns = [col.strip().lower() for col in df.columns]
        df.columns = ['Data Operação','Data valor','Tipo','Descrição','Débito' ,'Crédito', 'Saldo Controlo']
        df.rename(columns={
            'Data Operação': 'data',
            'Data valor': 'data_payment',
            'Tipo':'Tipo',
            'Descrição': 'lancamento',
            'Débito': 'DEBITO',
            'Crédito': 'CREDITO',
            'Saldo Controlo':'SALDO_CONTROLO'
        }, inplace=True)

        # Convert date column to datetime
        df['data_payment'] = pd.to_datetime(df['data_payment'], format='%d-%m-%Y', errors='coerce')
        df['data'] = pd.to_datetime(df['data'], format='%d-%m-%Y', errors='coerce')

        # Criar a coluna valor: Débito como negativo e Crédito como positivo
        df['DEBITO'] = pd.to_numeric(df['DEBITO'], errors='coerce').fillna(0)
        df['CREDITO'] = pd.to_numeric(df['CREDITO'], errors='coerce').fillna(0)

        df['valor'] = df['DEBITO'] + df['CREDITO']

        # Converter colunas de valores para numérico
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df['SALDO_CONTROLO'] = pd.to_numeric(df['SALDO_CONTROLO'], errors='coerce')

        # Drop rows where value is NaN (empty rows)
        df = df.dropna(how='all', subset=['valor'])

        # Forward fill dates para transações no mesmo dia
        df['data_payment'] = df['data_payment'].ffill()
        df['data'] = df['data'].ffill()

        # Sort by date (newest first)
        df = df.sort_values('data_payment', ascending=False)

        # Reset index
        df = df.reset_index(drop=True)

        return df
    
    def csvread(upload_csv):
        df = pd.read_csv(upload_csv)

        return df
    
    def pdfread(upload_pdf):
        pass
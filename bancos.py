import pandas as pd
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
        df = pd.read_excel(
            file_path,
            engine='openpyxl',
            sheet_name="Lançamentos",
            skiprows=10,  # Skip
            usecols="A:G",
            header=0 
        )

        # Clean column names
        df.columns = [col.strip().lower() for col in df.columns]
        df.columns = ['Data Operação','Data Valor','Tipo','Descrição','Débito' ,'Crédito', 'Saldo Controlo']
        df.rename(columns={
            'Data Operação': 'DATA_COMPETÊNCIA',
            'Data Valor': 'DATA_CAIXA',
            'Tipo':'Tipo',
            'Descrição': 'DESCRICAO',
            'Débito': 'DEBITO',
            'Crédito': 'CREDITO',
            'Saldo Controlo':'Saldo_Controlo'
        }, inplace=True)

        # Convert date column to datetime
        df['DATA_CAIXA'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
        df['DATA_COMPETÊNCIA'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

        # Criar a coluna VALOR: Débito como negativo e Crédito como positivo
        df['VALOR'] = df['CREDITO'].fillna(0) - df['DEBITO'].fillna(0)

        # Converter colunas de valores para numérico
        df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce')
        df['SALDO_CONTROLO'] = pd.to_numeric(df['SALDO_CONTROLO'], errors='coerce')

        # Drop rows where value is NaN (empty rows)
        df = df.dropna(how='all', subset=['VALOR'])

        # Forward fill dates para transações no mesmo dia
        df['DATA_CAIXA'] = df['DATA_CAIXA'].ffill()
        df['DATA_COMPETÊNCIA'] = df['DATA_COMPETÊNCIA'].ffill()

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
import pandas as pd
class Itau:
    def xlsread(file_path):
        df = pd.read_excel(
            file_path,
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
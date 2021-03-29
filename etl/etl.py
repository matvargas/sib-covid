import pandas as pd
from sqlalchemy import create_engine
import chardet

#Abre o csv como pandas dataframe
def get_dataframe(csvFile):
    df = pd.read_csv(csvFile, encoding='latin1', delimiter = ';')
    return df

def clean_dataframe(df):
    columns_to_delete = ['dataNascimento',
                         'paisOrigem',
                         'origem',
                         'excluido',
                         'validado']

    #Remove colunas
    df.drop(columns_to_delete, inplace=True, axis=1)

    #Remove linhas com colunas restantes nulas
    df.dropna(subset=['dataNotificacao'], inplace=True)
    df.dropna(subset=['sintomas'], inplace=True)
    df.dropna(subset=['sexo'], inplace=True)
    df.dropna(subset=['municipio'], inplace=True)
    df.dropna(subset=['municipioIBGE'], inplace=True)
    df.dropna(subset=['estadoNotificacao'], inplace=True)
    df.dropna(subset=['estadoNotificacaoIBGE'], inplace=True)
    df.dropna(subset=['municipioNotificacao'], inplace=True)
    df.dropna(subset=['municipioNotificacaoIBGE'], inplace=True)
    df.dropna(subset=['dataInicioSintomas'], inplace=True)
    df.dropna(subset=['profissionalSaude'], inplace=True)

#Formata a data para que o MySQL reconheça como tipo DATE
def format_date_values(df):
    df['dataNotificacao'] = pd.to_datetime(df['dataNotificacao']).dt.date
    df['dataInicioSintomas'] = pd.to_datetime(df['dataInicioSintomas']).dt.date
    df['dataEncerramento'] = pd.to_datetime(df['dataEncerramento']).dt.date
    df['dataTeste'] = pd.to_datetime(df['dataTeste']).dt.date

#Faz a conexão com o banco de dados e escreve os dados
def write_to_database(df, db_user, db_password, db_name, table_name):
    conn_str = "mysql+pymysql://{user}:{pw}@localhost/{db}".format(user=db_user, pw=db_password, db=db_name)
    engine = create_engine(conn_str)
    df.to_sql(table_name, con = engine, if_exists = 'append', chunksize = 1000, index=False)

if __name__ == "__main__":
    
    csv_files = ['../data/dados-mg-1.csv',
                 '../data/dados-mg-2.csv',
                 '../data/dados-mg-3.csv']
    
    for csv_file in csv_files:
        df = get_dataframe(csv_file)
        clean_dataframe(df)
        format_date_values(df)
        write_to_database(df, "sibcovid", "sibcovid", "sib_covid", "dados_covid_mg")

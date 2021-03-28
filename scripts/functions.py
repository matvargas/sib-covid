import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

from pandas import DataFrame

import numpy as np

import matplotlib.pyplot as plt

import folium

import circlify

import seaborn as sns

##Utilitarias

def get_db_connection(db_user, db_password, db_name):
    conn_str = "mysql+pymysql://{user}:{pw}@localhost/{db}".format(user=db_user, pw=db_password, db=db_name)
    engine = create_engine(conn_str)
    conn = engine.connect()
    return conn

def switch_city(argument):
    switcher = {
        "Belo Horizonte": 0,
        "Uberlï¿½ndia": 1,
        "Contagem": 2,
        "Betim": 3,
        "Ipatinga": 4,
        "Montes Claros": 5,
        "Uberaba": 6,
        "Juiz de Fora": 7,
        "Governador Valadares": 8,
        "Sete Lagoas": 9,
        "Pouso Alegre": 10,
        "Itabira": 11,
        "Divinï¿½polis": 12,
        "Nova Lima": 13,
        "Ubï¿½": 14,
        "Araguari": 15,
        "Muriaï¿½": 16,
        "Ouro Preto": 17,
        "Ibiritï¿½": 18,
        "Teï¿½filo Otoni": 19

    }
    return switcher.get(argument, "NULL") 

##Notificacoes

def graph_notifications_by_age(conn, min_age, max_age, min_date, max_date):
    sql = "SELECT idade, count(idade) from dados_covid_mg "
    sql = sql + "WHERE idade >= {min_age_value} AND idade <= {max_age_value} "
    sql = sql + "AND dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\" "
    sql = sql + "GROUP BY idade"
    
    sql = sql.format(min_age_value=min_age, 
                     max_age_value=max_age, 
                     min_date_value=min_date, 
                     max_date_value=max_date)

    rs = conn.execute(sql)
    df = DataFrame(rs.fetchall())
    df = df.rename(columns={0 : 'idade', 1 : 'notificacoes'})

    x_pos = np.arange(len(df['idade']))
    
    # Cria barras e escolhe a cor
    plt.bar(x_pos, df['notificacoes'], color = (0.5,0.1,0.5,0.6), width=0.2)
    
    # Adiciona titulo e label nos eixos
    plt.title('Notificações por idade (De ' + min_date + ' à ' + max_date + ')' )
    plt.xlabel('Idade')
    plt.ylabel('Notificações')
    
    # Cria nomes no eixo X
    plt.xticks(x_pos, df['idade'], rotation=90)
    
    # Mostra o grafico
    plt.show()

def top_20_cities_notifications(conn):
    sql = "SELECT municipioNotificacao, count(row_id) as cnt from dados_covid_mg GROUP BY municipioNotificacao ORDER BY cnt DESC LIMIT 21"
    m = folium.Map(location=[-19.8157,-43.9542], tiles="OpenStreetMap", zoom_start=6, width=1200, height=600)

    rs = conn.execute(sql)
    df = DataFrame(rs.fetchall())
    df = df.rename(columns={0 : 'municipio', 1 : 'notificacoes'})

    sum_notifications = 0
    for t in df.itertuples():
        sum_notifications = sum_notifications + t.notificacoes

    values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    notifications = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for t in df.itertuples():
        index = switch_city(t.municipio)
        if(index == "NULL"):
            continue
        values[int(index)] = (float(t.notificacoes)/float(sum_notifications))*20
        notifications[int(index)] = t.notificacoes
        
    lon = [-43.9542, 
           -48.2622, 
           -44.0529, 
           -44.1991, 
           -42.5367, 
           -43.8647, 
           -47.9325, 
           -43.3496, 
           -41.9481,
           -44.2477,
           -45.9332,
           -43.2121,
           -44.8872,
           -43.8463,
           -42.943,
           -48.1854,
           -42.3674,
           -43.5035,
           -44.0561,
           -41.509
           ]
    
    lat = [-19.8157, 
           -18.9113, 
           -19.9386, 
           -19.9676, 
           -19.469, 
           -16.737, 
           -19.7502, 
           -21.7642, 
           -18.8505,
           -19.4679,
           -22.2341,
           -19.6657,
           -20.1394,
           -19.9876,
           -21.1208,
           -18.651,
           -21.1303,
           -20.3856,
           -20.0194,
           -17.8588
           ]

    cities =  ['Belo Horizonte', 
               'Uberlândia', 
               'Contagem', 
               'Betim', 
               'Ipatinga', 
               'Montes Claros',
               'Uberaba',
               'Juiz de Fora',
               'Governador Valadares',
               'Sete Lagoas',
               'Pouso Alegre',
               'Itabira',
               'Divinópolis',
               'Nova Lima',
               'Ubá',
               'Araguari',
               'Muriaé',
               'Ouro Preto',
               'Ibirité',
               'Teófilo Otoni',
              ]

    data = pd.DataFrame({
    'lon':lon,
    'lat':lat,
    'name': cities,
    'value': values,
    }, dtype=str)

    for i in range(0,len(data)):
        folium.Circle(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=data.iloc[i]['name'] + " - Notificações: " + str(notifications[i]),
            radius=float(data.iloc[i]['value'])*20000,
            color='crimson',
            fill=True,
            fill_color='crimson'
        ).add_to(m)

    m.save('/home/arthur/sib-covid/covid_data_viewer/templates/mapstop_20_cities_notifications.html')

def graph_notifications_by_gender(conn, min_date, max_date):
    sql = "SELECT sexo, count(sexo) FROM dados_covid_mg "
    sql = sql + "WHERE dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\"  "
    sql = sql + "GROUP BY sexo"

    sql = sql.format(min_date_value=min_date, max_date_value=max_date)

    rs = conn.execute(sql)
    df = DataFrame(rs.fetchall())
    df = df.rename(columns={0 : 'genero', 1 : 'notificacoes'})

    x_pos = np.arange(len(df['genero']))
    
    # Cria barras e escolhe a cor
    plt.bar(x_pos, df['notificacoes'], color = (0.5,0.1,0.5,0.6), width=1)
    
    # Adiciona titulo e label nos eixos
    plt.title('Notificações por gênero (De ' + min_date + ' à ' + max_date + ')' )
    plt.xlabel('Gênero')
    plt.ylabel('Notificações')
    
    # Cria nomes no eixo X
    plt.xticks(x_pos, df['genero'], rotation=0)
    
    # Mostra o grafico
    plt.show()

##Testes

def test_results_by_date(conn, min_date, max_date):
    sql = "SELECT resultadoTeste, count(resultadoTeste) FROM dados_covid_mg "
    sql = sql + "WHERE resultadoTeste != \"NULL\" AND dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\"  "
    sql = sql + "AND resultadoTeste != \"Inconclusivo ou Indeterminado\"GROUP BY resultadoTeste"

    sql = sql.format(min_date_value=min_date, max_date_value=max_date)

    rs = conn.execute(sql)
    df = DataFrame(rs.fetchall())
    df = df.rename(columns={0 : 'Name', 1 : 'Value'})

    circles = circlify.circlify(
        df['Value'].tolist(), 
        show_enclosure=False, 
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )
    # Create just a figure and only one subplot
    fig, ax = plt.subplots(figsize=(10,10))

    # Title
    ax.set_title('Resultados dos Testes (De ' + min_date + ' à ' + max_date + ')')

    # Remove axes
    ax.axis('off')

    # Find axis boundaries
    lim = max(
        max(
            abs(circle.x) + circle.r,
            abs(circle.y) + circle.r,
        )
        for circle in circles
    )
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)

    # list of labels
    labels = df['Name']

    for circle, label in zip(circles, labels):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r*0.7, alpha=0.9, linewidth=2, facecolor="#69b2a3", edgecolor="black"))
        plt.annotate(label, (x,y ) ,va='center', ha='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round', pad=.5))

    plt.show()

#Casos confirmados

def evolution_of_cases(conn):
    sql = "select evolucaoCaso, dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Internado\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    internado = DataFrame(rs.fetchall())
    internado = internado.rename(columns={0 : 'evolucaoCaso', 1 : 'dataEncerramento', 2 : 'notificacoes'})

    sql = "select evolucaoCaso, dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Internado em UTI\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    internadoUTI = DataFrame(rs.fetchall())
    internadoUTI = internadoUTI.rename(columns={0 : 'evolucaoCaso', 1 : 'dataEncerramento', 2 : 'notificacoes'})

    sql = "select evolucaoCaso, dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Cura\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    cura = DataFrame(rs.fetchall())
    cura = cura.rename(columns={0 : 'evolucaoCaso', 1 : 'dataEncerramento', 2 : 'notificacoes'})

    sql = "select evolucaoCaso, dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"ï¿½bito\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    obito = DataFrame(rs.fetchall())
    obito = obito.rename(columns={0 : 'evolucaoCaso', 1 : 'dataEncerramento', 2 : 'notificacoes'})

    sql = "select evolucaoCaso, dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Em tratamento domiciliar\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    domiciliar = DataFrame(rs.fetchall())
    domiciliar = domiciliar.rename(columns={0 : 'evolucaoCaso', 1 : 'dataEncerramento', 2 : 'notificacoes'})

    df = ((((internado.append(internadoUTI, ignore_index=True)).append(obito, ignore_index=True)).append(cura, ignore_index=True)).append(domiciliar, ignore_index=True))

    print(df)
    
    # Create a grid : initialize it
    #g = sns.FacetGrid(df, col='evolucaoCaso', hue='evolucaoCaso', col_wrap=4, )

    # Add the line over the area with the plot function
    #g = g.map(plt.plot, 'dataEncerramento', 'notificacoes')
    
    # Fill the area with fill_between
    #g = g.map(plt.fill_between, 'dataEncerramento', 'notificacoes', alpha=0.2).set_titles("{col_name} evolucaoCaso")
    
    # Control the title of each facet
    #g = g.set_titles("{col_name}")
    
    # Add a title for the whole plot
    #plt.subplots_adjust(top=0.92)
    #g = g.fig.suptitle('Evolução dos casos notificados')

    # Show the graph
    #plt.show()

if __name__ == "__main__":
    db_user="root"
    db_password="@rthur96"
    db_name="sib_covid"

    conn = get_db_connection(db_user, db_password, db_name)

    min_age = 10
    max_age = 30
    min_date = "2020-01-01"
    max_date = "2021-02-02"

    #homepage
    #top_20_cities_notifications(conn)

    #notificacoes
    #graph_notifications_by_age(conn, min_age, max_age, min_date, max_date)
    #graph_notifications_by_gender(conn, min_date, max_date)

    #casos confirmados
    #graph_notifications_by_age(conn, min_age, max_age, min_date, max_date)
    #graph_notifications_by_gender(conn, min_date, max_date)

    #internacao
    #graph_notifications_by_age(conn, min_age, max_age, min_date, max_date)
    #graph_notifications_by_gender(conn, min_date, max_date)

    #óbitos
    #graph_notifications_by_age(conn, min_age, max_age, min_date, max_date)
    #graph_notifications_by_gender(conn, min_date, max_date)

    #testes
    #test_results_by_date(conn, min_date, max_date)

    #evolucao
    evolution_of_cases(conn)


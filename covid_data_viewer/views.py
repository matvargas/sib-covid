# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame

db_user="root"
db_password="@rthur96"
db_name="sib_covid"
min_date = "2020-01-01"
max_date = "2021-02-02"

def home(request):
      return render(
        request,
        'covid_data_viewer/home.html',
      )

def supported_datasets(request):
      return render(
        request,
        'covid_data_viewer/supported_datasets.html',
      )

def about_data(request):
      return render(
        request,
        'covid_data_viewer/about_data.html',
      )

def get_db_connection(db_user, db_password, db_name):
    conn_str = "mysql+pymysql://{user}:{pw}@localhost/{db}".format(user=db_user, pw=db_password, db=db_name)
    engine = create_engine(conn_str)
    conn = engine.connect()
    return conn



def get_notifications_by_age():
  conn = get_db_connection(db_user, db_password, db_name)
  sql = "SELECT idade, count(idade) from dados_covid_mg "
  sql = sql + "WHERE idade >= {min_age_value} AND idade <= {max_age_value} "
  sql = sql + "AND dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\" "
  sql = sql + "GROUP BY idade"
  
  min_age = 0
  max_age = 100

  sql = sql.format(min_age_value=min_age, 
                    max_age_value=max_age, 
                    min_date_value=min_date, 
                    max_date_value=max_date)

  rs = conn.execute(sql)
  df = DataFrame(rs.fetchall())
  df = df.rename(columns={0 : 'idade', 1 : 'notificacoes'})
  xaxis = df['idade'].tolist()
  yaxis = df['notificacoes'].tolist()
  return (xaxis, yaxis)

def get_notifications_by_gender():
  conn = get_db_connection(db_user, db_password, db_name)
  sql = "SELECT sexo, count(sexo) FROM dados_covid_mg "
  sql = sql + "WHERE dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\"  "
  sql = sql + "AND sexo != \"Indefinido\" "
  sql = sql + "GROUP BY sexo"
  sql = sql.format(min_date_value=min_date, max_date_value=max_date)

  rs = conn.execute(sql)
  df = DataFrame(rs.fetchall())
  df = df.rename(columns={0 : 'genero', 1 : 'notificacoes'})
  xaxis = df['genero'].tolist()
  yaxis = df['notificacoes'].tolist()
  return (xaxis, yaxis)

def get_notifications_by_date():
  conn = get_db_connection(db_user, db_password, db_name)
  sql = "SELECT dataNotificacao, count(dataNotificacao) FROM dados_covid_mg "
  sql = sql + "WHERE dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\"  "
  sql = sql + "GROUP BY dataNotificacao"
  
  sql = sql.format(min_date_value=min_date, max_date_value=max_date)

  rs = conn.execute(sql)
  df = DataFrame(rs.fetchall())
  df = df.rename(columns={0 : 'datas', 1 : 'notificacoes'})
  df['media_7_dias'] = df['notificacoes'].rolling(window=7).mean()

  xaxis = (df['datas'].astype(str)).tolist()
  yaxis = df['notificacoes'].tolist()
  yaxis_2 = (df['media_7_dias'].fillna(0)).tolist()
  return (xaxis, yaxis, yaxis_2)

def view_notifications(request):
  xaxis_n_age, yaxis_n_age = get_notifications_by_age()
  xaxis_n_gender, yaxis_n_gender = get_notifications_by_gender()
  xaxis_n_date, yaxis_n_date, yaxis_2_n_date = get_notifications_by_date()
  context={'xaxis_n_age' : xaxis_n_age, 
           'yaxis_n_age' : yaxis_n_age, 
           'xaxis_n_gender' : xaxis_n_gender, 
           'yaxis_n_gender' : yaxis_n_gender,
           'xaxis_n_date' : xaxis_n_date,
           'yaxis_n_date' : yaxis_n_date,
           'yaxis_2_n_date' : yaxis_2_n_date}
  return render(
    request,
    'covid_data_viewer/view_notifications.html',
    context
  )

def get_cases_by_age():
  conn = get_db_connection(db_user, db_password, db_name)
  sql = "SELECT idade, count(idade) from dados_covid_mg "
  sql = sql + "WHERE idade >= {min_age_value} AND idade <= {max_age_value} "
  sql = sql + "AND dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\" "
  sql = sql + " AND resultadoTeste =\"Positivo\""
  sql = sql + "GROUP BY idade"
  
  min_age = 0
  max_age = 100

  sql = sql.format(min_age_value=min_age, 
                   max_age_value=max_age, 
                   min_date_value=min_date, 
                   max_date_value=max_date)

  rs = conn.execute(sql)
  df = DataFrame(rs.fetchall())
  df = df.rename(columns={0 : 'idade', 1 : 'notificacoes'})
  xaxis = df['idade'].tolist()
  yaxis = df['notificacoes'].tolist()
  return (xaxis, yaxis)

def get_cases_by_gender():
  conn = get_db_connection(db_user, db_password, db_name)
  sql = "SELECT sexo, count(sexo) FROM dados_covid_mg "
  sql = sql + "WHERE dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\"  "
  sql = sql + "AND sexo != \"Indefinido\" AND resultadoTeste =\"Positivo\" "
  sql = sql + "GROUP BY sexo"
  sql = sql.format(min_date_value=min_date, max_date_value=max_date)

  rs = conn.execute(sql)
  df = DataFrame(rs.fetchall())
  df = df.rename(columns={0 : 'genero', 1 : 'notificacoes'})
  xaxis = df['genero'].tolist()
  yaxis = df['notificacoes'].tolist()
  return (xaxis, yaxis)

def get_cases_by_date():
  conn = get_db_connection(db_user, db_password, db_name)
  sql = "SELECT dataNotificacao, count(dataNotificacao) FROM dados_covid_mg "
  sql = sql + "WHERE dataNotificacao >= \"{min_date_value}\" AND dataNotificacao <= \"{max_date_value}\"  AND resultadoTeste =\"Positivo\" "
  sql = sql + "GROUP BY dataNotificacao"
  
  sql = sql.format(min_date_value=min_date, max_date_value=max_date)

  rs = conn.execute(sql)
  df = DataFrame(rs.fetchall())
  df = df.rename(columns={0 : 'datas', 1 : 'notificacoes'})
  df['media_7_dias'] = df['notificacoes'].rolling(window=7).mean()

  xaxis = (df['datas'].astype(str)).tolist()
  yaxis = df['notificacoes'].tolist()
  yaxis_2 = (df['media_7_dias'].fillna(0)).tolist()
  return (xaxis, yaxis, yaxis_2)

def view_cases(request):
  xaxis_c_age, yaxis_c_age = get_cases_by_age()
  xaxis_c_gender, yaxis_c_gender = get_cases_by_gender()
  xaxis_c_date, yaxis_c_date, yaxis_2_c_date = get_cases_by_date()
  context={'xaxis_c_age' : xaxis_c_age, 
           'yaxis_c_age' : yaxis_c_age, 
           'xaxis_c_gender' : xaxis_c_gender, 
           'yaxis_c_gender' : yaxis_c_gender,
           'xaxis_c_date' : xaxis_c_date,
           'yaxis_c_date' : yaxis_c_date,
           'yaxis_2_c_date' : yaxis_2_c_date}
  return render(
    request,
    'covid_data_viewer/view_cases.html',
    context
  )
  
def get_evolution_by_date():
    conn = get_db_connection(db_user, db_password, db_name)
    sql = "select dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Internado\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    internado = DataFrame(rs.fetchall())
    internado = internado.rename(columns={0 : 'dataEncerramento', 1 : 'notificacoes'})
    internado['media_7_dias'] = ((internado['notificacoes'].rolling(window=7).mean()).fillna(0))

    sql = "select dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Internado em UTI\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    internadoUTI = DataFrame(rs.fetchall())
    internadoUTI = internadoUTI.rename(columns={0 : 'dataEncerramento', 1 : 'notificacoes'})
    internadoUTI['media_7_dias'] = ((internadoUTI['notificacoes'].rolling(window=7).mean()).fillna(0))


    sql = "select dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Cura\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    cura = DataFrame(rs.fetchall())
    cura = cura.rename(columns={0 : 'dataEncerramento', 1 : 'notificacoes'})
    cura['media_7_dias'] = ((cura['notificacoes'].rolling(window=7).mean()).fillna(0))
    print(cura)

    sql = "select dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"ï¿½bito\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    obito = DataFrame(rs.fetchall())
    obito = obito.rename(columns={0 : 'dataEncerramento', 1 : 'notificacoes'})
    obito['media_7_dias'] = ((obito['notificacoes'].rolling(window=7).mean()).fillna(0))


    sql = "select dataEncerramento, count(evolucaoCaso) from dados_covid_mg where evolucaoCaso = \"Em tratamento domiciliar\" and dataEncerramento != \"NULL\" group by dataEncerramento;"
    rs = conn.execute(sql)
    domiciliar = DataFrame(rs.fetchall())
    domiciliar = domiciliar.rename(columns={0 : 'dataEncerramento', 1 : 'notificacoes'})
    domiciliar['media_7_dias'] = ((domiciliar['notificacoes'].rolling(window=7).mean()).fillna(0))

    internado_x = (internado['dataEncerramento'].astype(str)).tolist()
    internado_y = internado['notificacoes'].tolist()
    internado_y_media = internado['media_7_dias'].tolist()


    uti_x = (internadoUTI['dataEncerramento'].astype(str)).tolist()
    uti_y = internadoUTI['notificacoes'].tolist()
    uti_y_media = internadoUTI['media_7_dias'].tolist()

    cura_x = (cura['dataEncerramento'].astype(str)).tolist()
    cura_y = cura['notificacoes'].tolist()
    cura_y_media = cura['media_7_dias'].tolist()


    obito_x = (obito['dataEncerramento'].astype(str)).tolist()
    obito_y = obito['notificacoes'].tolist()
    obito_y_media = obito['media_7_dias'].tolist()


    domiciliar_x = (domiciliar['dataEncerramento'].astype(str)).tolist()
    domiciliar_y = domiciliar['notificacoes'].tolist()
    domiciliar_y_media = domiciliar['media_7_dias'].tolist()

    return (internado_x, internado_y, internado_y_media, uti_x, uti_y, uti_y_media, cura_x, cura_y, cura_y_media, obito_x, obito_y, obito_y_media, domiciliar_x, domiciliar_y, domiciliar_y_media)

def view_evolution(request):
  internado_x, internado_y, internado_y_media, uti_x, uti_y, uti_y_media, cura_x, cura_y, cura_y_media, obito_x, obito_y, obito_y_media, domiciliar_x, domiciliar_y, domiciliar_y_media = get_evolution_by_date()
  context={'internado_x' : internado_x, 
           'internado_y' : internado_y, 
           'internado_y_media' : internado_y_media, 
           'uti_x' : uti_x, 
           'uti_y' : uti_y,
           'uti_y_media' : uti_y_media,
           'cura_x' : cura_x,
           'cura_y' : cura_y,
           'cura_y_media' : cura_y_media,
           'obito_x' : obito_x,
           'obito_y' : obito_y,
           'obito_y_media' : obito_y_media,
           'domiciliar_x' : domiciliar_x,
           'domiciliar_y' : domiciliar_y,
           'domiciliar_y_media' : domiciliar_y_media}
  return render(
    request,
    'covid_data_viewer/view_evolution.html',
    context
  )
  
def contact(request):
      return render(
        request,
        'covid_data_viewer/contact.html',
      )

#load rds dataset
import psycopg2
import boto3
import configparser
import pandas as pd
import numpy as np

def connect_db():
    cfg = configparser.ConfigParser()
    cfg.read('tmp.ini')
    
    dbname = cfg['PGCONNECT']['dbname']
    host = cfg['PGCONNECT']['host']
    port = cfg['PGCONNECT']['port']
    user = cfg['PGCONNECT']['user']
    password = cfg['PGCONNECT']['password']

    try:
        conn = psycopg2.connect(
            dbname=dbname, 
            host=host, 
            port=port, 
            user=user, 
            password=password
        )
        conn.autocommit = True
    except:
        print('Unable to connect to the database.')
    
    cur = conn.cursor()
    cur.execute('SELECT * FROM nascar_linestar')

    df = []
    for row in cur.fetchall():
        df.append(row)

    #put into dataframe
    cur.execute("SELECT * FROM nascar_linestar LIMIT 0")
    df = pd.DataFrame(df, columns=[x[0] for x in cur.description])

    return df
    
data_clean():
    df = connect_db()
predictors = [
    'name',
    'sal',
    'gt',
    'pp',
    'races',
    'wins',
    'top_fives',
    'top_tens',
    'avg_finish',
    'laps_led_race',
    'fastest_laps_race',
    'avg_pass_diff',
    'quality_passes_race',
    'fppg',
    'practice_laps',
    'practice_best_lap_time',
    'practice_best_lap_speed',
    'qualifying_pos',
    'qualifying_best_lap_time',
    'qualifying_best_lap_speed',
    'laps',
    'miles',
    'surface',
    'restrictor_plate',
    'cautions_race',
    'finished',
    'top_5s',
    'top_10s',
    'avg_place'
]

label = ['ps']

tmp_df = df[label+predictors].dropna()

def data_transform(df):
    
    for col in df.columns:
        if col not in ['gt', 'name', 'restrictor_plate', 'surface']:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                print(col, 'not numeric.')
                
    df = pd.get_dummies(df, columns=['name', 'restrictor_plate', 'surface'], drop_first=True)
    df['gt'] = pd.to_datetime(df['gt']).dt.date  
    
    return df

tmp = data_transform(tmp_df)
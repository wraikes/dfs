#load rds dataset
import psycopg2
import configparser
import pandas as pd
import numpy as np

cfg = configparser.ConfigParser()
cfg.read('./tmp.ini')

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
    
df = pd.DataFrame(df)    
df.columns = [cur.description[i][0] for i in range(len(cur.description))]

label = ['ps']
predictors = [
    'name',
    'sal',
    'race_date',
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
    'races_3',
    'finished',
    'wins_3',
    'top_5s',
    'top_10s',
    'avg_place',
    'races_4',
    'finished_4',
    'wins_4',
    'top_5s_4',
    'top_10s_4',
    'avg_place_4'
]

df = df[label+predictors].dropna()

def data_transform(df):
    
    for col in df.columns:
        if col not in ['race_date', 'name', 'restrictor_plate', 'surface']:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                print(col, 'not numeric.')
    
    df['_name'] = df['name']            
    df = pd.get_dummies(df, columns=['name', 'restrictor_plate', 'surface'], drop_first=True)
    df['race_date'] = pd.to_datetime(df['race_date']).dt.date  
    
    return df

df = data_transform(df)
df.to_csv('./tmp.csv')




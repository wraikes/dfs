#load rds dataset
import psycopg2
import configparser
import pandas as pd
import numpy as np


class LoadData:
    def __init__(self, config_file, db_name, label, predictors, non_numeric_cols):
        self.config_file = config_file
        self.db_name = db_name
        self.label = label
        self.predictors = predictors
        self.non_numeric_cols = non_numeric_cols
        
        self.cursor = None
        self.df = []


    def setup_connection(self):
        cfg = configparser.ConfigParser()
        cfg.read(self.config_file)
    
        dbname = cfg['PGCONNECT']['dbname']
        host = cfg['PGCONNECT']['host']
        port = cfg['PGCONNECT']['port']
        user = cfg['PGCONNECT']['user']
        password = cfg['PGCONNECT']['password']
    
        conn = psycopg2.connect(
            dbname=dbname, 
            host=host, 
            port=port, 
            user=user, 
            password=password
        )
        
        conn.autocommit = True
        self.cursor = conn.cursor()


    def create_df(self):

        self.cursor.execute('SELECT * FROM {}'.format(self.db_name))
        for row in self.cursor.fetchall():
            self.df.append(row)
    
        self.df = pd.DataFrame(self.df)
        self.df.columns = [self.cursor.description[i][0] for i in range(len(self.cursor.description))]

     
    def data_clean(self):
        self.df = self.df[self.label+self.predictors].dropna() 

        for col in self.df.columns:
            if col not in non_numeric_cols:
                self.df[col] = pd.to_numeric(self.df[col])
    
        self.df['_name'] = self.df['name']            
        self.df = pd.get_dummies(df, columns=['_name', 'restrictor_plate', 'surface'], drop_first=True)
        self.df['race_date'] = pd.to_datetime(self.df['race_date']).dt.date  
    
        
non_numeric_cols = [
    'race_date',
    'name', 
    'restrictor_plate',
    'surface'
]
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




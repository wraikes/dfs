#load rds dataset
import psycopg2
import configparser
import pandas as pd
import numpy as np


class LoadData:
    def __init__(self, config_file, db_name):
        self.config_file = config_file
        self.db_name = db_name
        self.df = []
        self.cursor = None


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

     
    def data_clean(self, non_numeric_cols, predictors, label=['ps']):
        self.df = self.df[label+predictors].dropna() 

        for col in self.df.columns:
            if col not in non_numeric_cols:
                self.df[col] = pd.to_numeric(self.df[col])
    
        #self.df['_name'] = self.df['name']            
        #self.df = pd.get_dummies(self.df, columns=['_name', 'restrictor_plate', 'surface'], drop_first=True)
        #self.df['race_date'] = pd.to_datetime(self.df['race_date']).dt.date  
    
        return self.df

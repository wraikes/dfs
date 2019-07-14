

#load rds dataset
import psycopg2
import boto3
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

#put into dataframe
cur.execute("SELECT * FROM nascar_linestar LIMIT 0")
df = pd.DataFrame(df, columns=[x[0] for x in cur.description])

#clean data / create new features
#####all decimal data read into as object...


#setup backtest
#setup integer programming optimizer (pulp)
#select best model based on backtested optimizer results
    
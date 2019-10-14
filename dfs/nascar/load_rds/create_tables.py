#create nascar tables; script only runs once
import boto3
import pandas as pd
import numpy as np
import json
import configparser
import psycopg2

from sql_queries import *

cfg = configparser.ConfigParser()
cfg.read('../database_creds.ini')
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
cur.execute('DROP TABLE IF EXISTS nascar_linestarapp')
cur.execute('DROP TABLE IF EXISTS nascar_sportsline_leaderboard')
cur.execute('DROP TABLE IF EXISTS nascar_sportsline_betting')
cur.execute('DROP TABLE IF EXISTS nascar_sportsline_dfs_pro')
    
cur.execute(nascar_linestarapp_create_table)
cur.execute(nascar_sportsline_dfs_pro_create_table)
cur.execute(nascar_sportsline_betting_create_table)
cur.execute(nascar_sportsline_leaderboard_create_table)

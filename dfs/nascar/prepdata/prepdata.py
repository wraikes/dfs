import pandas as pd
import psycopg2
import configparser
import boto3
import numpy as np

#load all databases
#clean all databases for merge
#merge all databases into one pandas dataframe

def connect_to_database():
    cfg = configparser.ConfigParser()
    cfg.read('../../database_creds.ini')
    
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
    return conn.cursor()


def load_linestarapp():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_linestarapp")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return df
    

def load_sportsline_leaderboard():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_sportsline_leaderboard")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return df


def load_sportsline_betting():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_sportsline_betting")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return df


def load_sportsline_dfs_pro():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_sportsline_dfs_pro")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return df







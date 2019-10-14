import boto3
import pandas as pd
import json
import configparser
import psycopg2

from etl_linestarapp import LinestarappETL
from etl_sportsline import _sportsline_leaderboard_data
from etl_sportsline import _insert_sportsline_leaderboard
from etl_sportsline import _sportsline_betting_data
from etl_sportsline import _insert_sportsline_betting
from etl_sportsline import _sportsline_dfs_pro_data
from etl_sportsline import _insert_sportsline_dfs_pro

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



def sportsline_main(cur):

    links = []
    cur.execute('SELECT DISTINCT link FROM nascar_sportsline_betting')
    [links.append(link[0]) for link in cur.fetchall()]
    cur.execute('SELECT DISTINCT link FROM nascar_sportsline_dfs_pro')
    [links.append(link[0]) for link in cur.fetchall()]
    cur.execute('SELECT DISTINCT link FROM nascar_sportsline_leaderboard')
    [links.append(link[0]) for link in cur.fetchall()]
    
    #initialize bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    # loop thru bucket and extract data
    for obj in bucket.objects.filter(Prefix='{}/{}/'.format('nascar', 'sportsline')):
        #skip objects if folder or projection data
        if obj.key[-1] == '/':
            continue
        
        #if file pid not in rds pid keys, pull file, else continue        
        link = obj.key.split('/')[-1]
        
        if link in links:
            continue
        else:
            file = s3.Object('my-dfs-data', obj.key)
            data = file.get()['Body'].read()
            data = json.loads(data)
        print(link)        
        if 'leaderboard' in link: 
            data = _sportsline_leaderboard_data(data)
            _insert_sportsline_leaderboard(cur, link, data)
            
        elif 'dfs-pro' in link:
            data = _sportsline_dfs_pro_data(data)
            _insert_sportsline_dfs_pro(cur, link, data)
            
        elif 'betting' in link:
            data = _sportsline_betting_data(data)
            _insert_sportsline_betting(cur, link, data)


def linestarapp_main(cur):

    #pid's used to append new data
    cur.execute('SELECT race_id FROM nascar_linestarapp')
    pids = set(x[0] for x in cur.fetchall())
    
    #initialize bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    # loop thru bucket and extract data
    for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format('nascar', 'linestarapp', 'fd')):
        #skip objects if folder or projection data
        if obj.key[-1] == '/' or 'projections' in obj.key:
            continue
        
        #if file pid not in rds pid keys, pull file, else continue        
        pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
        if pid in pids:
            continue
        else:    
            file = s3.Object('my-dfs-data', obj.key)
            data = file.get()['Body'].read()
            data = json.loads(data)
        
        #transform file into usable dictionary
        etl = LinestarappETL(cur)
        data_cache = etl.transform_linestarapp(data)
        
        #load dict into rds as new record
        for player_id in data_cache[pid]:
            etl.insert_linestarapp(data_cache[pid][player_id], pid)
            
        
if __name__ == '__main__':
    cur = connect_to_database()
    linestarapp_main(cur)
    sportsline_main(cur)

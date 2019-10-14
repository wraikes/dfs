import boto3
import json
import pandas as pd
import numpy as np
import configparser
import psycopg2

from sql_queries import *


def _connect_to_database():
    cfg = configparser.ConfigParser()
    cfg.read('../database_creds.ini')
    
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


def _sportsline_leaderboard_data(file):
    cache = {}

    cache['title'] = file['metaData']['headline']
    cache['date'] = file['metaData']['timestamp']
    
    positions = [x.split('<br>')[0] for x in file['metaData']['body'].split('\t')[1:]]    
    for i, pos in enumerate(positions):
        cache['pos_{}'.format(i)] = pos
    
    return cache


def _sportsline_dfs_pro_data(file):
    cache = {}
    
    cache['title'] = file['details']['title']
    cache['date'] = file['details']['content_date']
    
    positions = []
    try:
        positions = [x.split('<br>')[0] for x in file['details']['body'].split('\t')[1:]]
    except:
        pass
    
    if len(positions) < 5:
        try:
            positions = [x for x in file['details']['body'].split('</strong></p><p>')[1].split('</p><p>') if not x.startswith('<em>')]
        except:
            pass
        
    if len(positions) < 5:
        try:
            positions = [x for x in data['details']['body'].split('<br>') if '$' in x][1:]
        except:
            pass
        
    print(len(positions))
    for i, pos in enumerate(positions):
        cache['pos_{}'.format(i)] = pos

    return cache
    
    
def _sportsline_betting_data(file):
    cache = {}
    
    cache['title'] = file['details']['title']
    cache['date'] = file['details']['content_date']
    
    positions = [x.split(' -')[0].split('</str')[0] for x in file['details']['body'].split('#')[1:]]
    
    for i, pos in enumerate(positions):
        cache['pos_{}'.format(i)] = pos

    return cache
    
    
def _insert_sportsline_dfs_pro(cur, link, data):
    cur.execute(nascar_sportsline_dfs_pro_insert, (
        link,
        data['title'],
        data['date'],
        data['pos_1'] if 'pos_1' in data.keys() else np.nan,
        data['pos_2'] if 'pos_2' in data.keys() else np.nan,
        data['pos_3'] if 'pos_3' in data.keys() else np.nan,
        data['pos_4'] if 'pos_4' in data.keys() else np.nan,
        data['pos_5'] if 'pos_5' in data.keys() else np.nan,
        data['pos_6'] if 'pos_6' in data.keys() else np.nan,
        data['pos_7'] if 'pos_7' in data.keys() else np.nan,
        data['pos_8'] if 'pos_8' in data.keys() else np.nan,
        data['pos_9'] if 'pos_9' in data.keys() else np.nan,
        data['pos_10'] if 'pos_10' in data.keys() else np.nan,
        data['pos_11'] if 'pos_11' in data.keys() else np.nan
        )
)


def _insert_sportsline_betting(cur, link, data):
    cur.execute(nascar_sportsline_betting_insert, (
        link,
        data['title'],
        data['date'],
        data['pos_1'] if 'pos_1' in data.keys() else np.nan,
        data['pos_2'] if 'pos_2' in data.keys() else np.nan,
        data['pos_3'] if 'pos_3' in data.keys() else np.nan,
        data['pos_4'] if 'pos_4' in data.keys() else np.nan,
        data['pos_5'] if 'pos_5' in data.keys() else np.nan,
        data['pos_6'] if 'pos_6' in data.keys() else np.nan,
        data['pos_7'] if 'pos_7' in data.keys() else np.nan,
        data['pos_8'] if 'pos_8' in data.keys() else np.nan,
        data['pos_9'] if 'pos_9' in data.keys() else np.nan,
        data['pos_10'] if 'pos_10' in data.keys() else np.nan,
        data['pos_11'] if 'pos_11' in data.keys() else np.nan,
        data['pos_12'] if 'pos_12' in data.keys() else np.nan,
        data['pos_13'] if 'pos_13' in data.keys() else np.nan,
        data['pos_14'] if 'pos_14' in data.keys() else np.nan,
        data['pos_15'] if 'pos_15' in data.keys() else np.nan,
        data['pos_16'] if 'pos_16' in data.keys() else np.nan,
        data['pos_17'] if 'pos_17' in data.keys() else np.nan,
        data['pos_18'] if 'pos_18' in data.keys() else np.nan,
        data['pos_19'] if 'pos_19' in data.keys() else np.nan,
        data['pos_20'] if 'pos_20' in data.keys() else np.nan
    )
)


def _insert_sportsline_leaderboard(cur, link, data):
    cur.execute(nascar_sportsline_leaderboard_insert, (
        link,
        data['title'],
        data['date'],
        data['pos_1'] if 'pos_1' in data.keys() else np.nan,
        data['pos_2'] if 'pos_2' in data.keys() else np.nan,
        data['pos_3'] if 'pos_3' in data.keys() else np.nan,
        data['pos_4'] if 'pos_4' in data.keys() else np.nan,
        data['pos_5'] if 'pos_5' in data.keys() else np.nan,
        data['pos_6'] if 'pos_6' in data.keys() else np.nan,
        data['pos_7'] if 'pos_7' in data.keys() else np.nan,
        data['pos_8'] if 'pos_8' in data.keys() else np.nan,
        data['pos_9'] if 'pos_9' in data.keys() else np.nan,
        data['pos_10'] if 'pos_10' in data.keys() else np.nan,
        data['pos_11'] if 'pos_11' in data.keys() else np.nan,
        data['pos_12'] if 'pos_12' in data.keys() else np.nan,
        data['pos_13'] if 'pos_13' in data.keys() else np.nan,
        data['pos_14'] if 'pos_14' in data.keys() else np.nan,
        data['pos_15'] if 'pos_15' in data.keys() else np.nan,
        data['pos_16'] if 'pos_16' in data.keys() else np.nan,
        data['pos_17'] if 'pos_17' in data.keys() else np.nan,
        data['pos_18'] if 'pos_18' in data.keys() else np.nan,
        data['pos_19'] if 'pos_19' in data.keys() else np.nan,
        data['pos_20'] if 'pos_20' in data.keys() else np.nan,
        data['pos_21'] if 'pos_21' in data.keys() else np.nan,
        data['pos_22'] if 'pos_22' in data.keys() else np.nan,
        data['pos_23'] if 'pos_23' in data.keys() else np.nan,
        data['pos_24'] if 'pos_24' in data.keys() else np.nan,
        data['pos_25'] if 'pos_25' in data.keys() else np.nan,
        data['pos_26'] if 'pos_26' in data.keys() else np.nan,
        data['pos_27'] if 'pos_27' in data.keys() else np.nan,
        data['pos_28'] if 'pos_28' in data.keys() else np.nan,
        data['pos_29'] if 'pos_29' in data.keys() else np.nan,
        data['pos_30'] if 'pos_30' in data.keys() else np.nan,
        data['pos_31'] if 'pos_31' in data.keys() else np.nan,
        data['pos_32'] if 'pos_32' in data.keys() else np.nan,
        data['pos_33'] if 'pos_33' in data.keys() else np.nan,
        data['pos_34'] if 'pos_34' in data.keys() else np.nan,
        data['pos_35'] if 'pos_35' in data.keys() else np.nan,
        data['pos_36'] if 'pos_36' in data.keys() else np.nan,
        data['pos_37'] if 'pos_37' in data.keys() else np.nan,
        data['pos_38'] if 'pos_38' in data.keys() else np.nan,
        data['pos_39'] if 'pos_39' in data.keys() else np.nan,
        data['pos_40'] if 'pos_40' in data.keys() else np.nan
    )
)


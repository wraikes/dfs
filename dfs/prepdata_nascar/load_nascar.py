import boto3
import json
import pandas as pd
import configparser
import psycopg2

from sql_queries import nascar_linestarapp_insert


def insert_nascar_data(cur, data, race_id, source=='linestarapp'):
    cur = _connect_to_database()
    
    if source=='linestarapp':
        _insert_linestarapp(cur, data, race_id)
    
    else:
        _insert_sportsline(cur, data, race_id)


def _connect_to_database():
    cfg = configparser.ConfigParser()
    cfg.read('./database_creds.ini')
    
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
    

def _insert_linestarapp(cur, data, race_id):
    cur.execute(nascar_linestarapp_insert,
        (
            race_id,
            data['S'],
            data['PID'],
            data['Name'],
            data['POS'],
            data['SAL'],
            data['GID'],
            data['GI'],
            data['GT'],
            data['PPG'],
            data['PP'],
            data['PS'],
            data['SS'],
            data['STAT'],
            data['IS'],
            data['Notes'],
            data['Floor'],
            data['Ceil'],
            data['Conf'],
            data['PTID'],
            data['OTID'],
            data['HTID'],
            data['OE'],
            data['OppRank'],
            data['OppTotal'],
            data['DSPID'],
            data['DGID'],
            data['IMG'],
            data['PTEAM'],
            data['HTEAM'],
            data['OTEAM'],
            data['Lock'],
            data['Id'],
            float(data['Races']),
            float(data['Wins']),
            float(data['Top Fives']),
            float(data['Top Tens']),
            float(data['Avg Finish']),
            float(data['Laps Led/Race']),
            float(data['Fastest Laps/Race']),
            float(data['Avg Pass Diff']),
            float(data['Quality Passes/Race']),
            float(data['FPPG']),
            float(data['Practice Laps']),
            float(data['Practice Best Lap Time']),
            float(data['Practice Best Lap Speed']),
            float(data['Qualifying Pos']) if data['Qualifying Pos'] != '-' else None,
            float(data['Qualifying Best Lap Time']),
            float(data['Qualifying Best Lap Speed']),
            float(data['Laps']),
            float(data['Miles']),
            data['Surface'],
            data['Restrictor Plate?'],
            float(data['Cautions/Race']),
            float(data['Races_3']),
            float(data['Finished']),
            float(data['Wins_3']),
            float(data['Top 5s']),
            float(data['Top 10s']),
            float(data['Avg. Place']),
            float(data['Races_4']),
            float(data['Finished_4']),
            float(data['Wins_4']),
            float(data['Top 5s_4']),
            float(data['Top 10s_4']),
            float(data['Avg. Place_4']),
            float(data['Owned']),
            float(data['SalaryId']),
            float(data['LoveCount']) if data['LoveCount'] else 0,
            float(data['HateCount']) if data['HateCount'] else 0
        )
    )


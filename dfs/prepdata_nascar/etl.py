import boto3
import json
import pandas as pd
import configparser
import psycopg2

from sql_queries import linestarapp_insert


def transform(json_data, source=='linestarapp'):
    data_cache = {}
    
    if source=='linestarapp':
        data_cache = _linestarapp_salary_data(data_cache, json_data)
        data_cache = _linestarapp_matchup_data(data_cache, json_data)
        data_cache = _linestarapp_ownership_data(data_cache, json_data)

    return data_cache
    

def _linestarapp_salary_data(data_cache, json_data):
    new_cache = data_cache.copy()
    race_id = json_data['Ownership']['PeriodId']
    new_cache[race_id] = {}
    
    for player_data in json_data['Ownership']['Salaries']:
        player_id = player_data['PID']
        new_cache[race_id][player_id] = player_data

    return new_cache
    

def _linestarapp_matchup_data(data_cache, json_data):
    new_cache = data_cache.copy()
    race_id = json_data['Ownership']['PeriodId']
  
    for i, table in enumerate(json_data['MatchupData']):
        col_names = table['Columns']
        id_store = []
        
        for player in table['PlayerMatchups']:
            player_id = player['PlayerId']
            
            if player_id in id_store or player_id not in new_cache[race_id].keys(): #why wouldn't it be in the data_cache?
                continue
            else:
                id_store.append(player_id)
            
            player_dict = dict(zip(col_names, player['Values']))
            
            for key, value in player_dict.items():
                if key in new_cache[race_id][player_id].keys():
                    new_cache[race_id][player_id]['{}_{}'.format(key, i)] = value                 
                else:
                    new_cache[race_id][player_id][key] = value
                    
    return new_cache
                
                
def _linestarapp_ownership_data(data_cache, json_data):
    new_cache = data_cache.copy()
    race_id = json_data['Ownership']['PeriodId']
        
    proj_key = list(json_data['Ownership']['Projected'].keys())[0]
    
    for player_id in new_cache[race_id].keys():
        for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
            new_cache[race_id][player_id][key] = None
    
    for player in json_data['Ownership']['Projected'][proj_key]:
        player_id = player['PlayerId']
        new_cache[race_id][player_id]['SalaryId'] = player['SalaryId']
        new_cache[race_id][player_id]['Owned'] = player['Owned']
    
    for player_id in new_cache[race_id].keys():
        if new_cache[race_id][player_id]['SalaryId']:
            salary_id = new_cache[race_id][player_id]['SalaryId']
            for player in json_data['AvgAdjustments']:
                if salary_id == player['SalaryId']:
                    for key in ['HateCount', 'LoveCount']:
                        new_cache[race_id][player_id][key] = player[key]
                        
    return new_cache


def load(cur, data, race_id, source=='linestarapp'):
    cur = _connect_to_database()
    
    if source=='linestarapp':
        _insert_linestarapp(cur, data, race_id)
    
    else:
        _insert_sportsline(cur, data, race_id)


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


def _insert_sportsline():
    pass
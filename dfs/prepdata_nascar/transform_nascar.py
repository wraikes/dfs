import boto3
import json
import pandas as pd


def extract_nascar_linestarapp(data_cache, json_data, source=='linestarapp'):
    new_cache = data_cache.copy()
    
    if source=='linestarapp':
        new_cache = _extract_salary_data(new_cache, json_data)
        new_cache = _extract_matchup_data(new_cache, json_data)
        new_cache = _extract_ownership_data(new_cache, json_data)

    return new_cache
    

def _extract_salary_data(data_cache, json_data):
    new_cache = data_cache.copy()
    race_id = json_data['Ownership']['PeriodId']
    new_cache[race_id] = {}
    
    for player_data in json_data['Ownership']['Salaries']:
        player_id = player_data['PID']
        new_cache[race_id][player_id] = player_data

    return new_cache
    

def _extract_matchup_data(data_cache, json_data):
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
                
                
def _extract_ownership_data(data_cache, json_data):
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



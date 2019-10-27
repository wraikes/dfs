import boto3
import json
import pandas as pd
import configparser
import psycopg2

class LinestarappETL:
    def __init__(self):
        pass


    def transform_linestarapp(self, json_data):
        data_cache = {}
        
        data_cache = self._linestarapp_salary_data(data_cache, json_data)
        data_cache = self._linestarapp_matchup_data(data_cache, json_data)
        data_cache = self._linestarapp_ownership_data(data_cache, json_data)
    
    
        df = pd.DataFrame.from_dict(
            {(i,j): data_cache[i][j] 
            for i in data_cache.keys() 
            for j in data_cache[i].keys()},
            orient='index'
        )
    
        return df
    

    def _linestarapp_salary_data(self, data_cache, json_data):
        new_cache = data_cache.copy()
        race_id = json_data['Ownership']['PeriodId']
        new_cache[race_id] = {}
        
        for player_data in json_data['Ownership']['Salaries']:
            player_id = player_data['PID']
            new_cache[race_id][player_id] = player_data
    
        return new_cache
    

    def _linestarapp_matchup_data(self, data_cache, json_data):
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
                    
                
    def _linestarapp_ownership_data(self, data_cache, json_data):
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
        
import boto3
import json
import re
import pandas as pd
import configparser
import psycopg2
from datetime import datetime

class LinestarappETL:
    
    def __init__(self):
        pass


    def transform_linestarapp(self, json_data, projections):
        data_cache = {}
        
        data_cache = self._linestarapp_salary_data(data_cache, json_data)
        data_cache = self._linestarapp_matchup_data(data_cache, json_data)
        data_cache = self._linestarapp_ownership_data(data_cache, json_data)
        data_cache = self._add_projections(data_cache, json_data, projections)
    
        return data_cache
    
    def _add_projections(self, data_cache, json_data, projections):
        event_id = json_data['Ownership']['PeriodId']
        
        for player in data_cache[event_id]:
            data_cache[event_id][player]['projections'] = projections
            
        return data_cache
    

    def _linestarapp_salary_data(self, data_cache, json_data):
        new_cache = data_cache.copy()
        event_id = json_data['Ownership']['PeriodId']
        new_cache[event_id] = {}
        
        for player_data in json_data['Ownership']['Salaries']:
            player_id = player_data['PID']
            player_data['GT'] = datetime.strptime(player_data['GT'].split('T')[0], '%Y-%m-%d')
            new_cache[event_id][player_id] = player_data

        return new_cache
    

    def _linestarapp_matchup_data(self, data_cache, json_data):
        new_cache = data_cache.copy()
        event_id = json_data['Ownership']['PeriodId']
      
        for i, table in enumerate(json_data['MatchupData']):
            col_names = table['Columns']
            id_store = []
            
            for player in table['PlayerMatchups']:
                player_id = player['PlayerId']
                
                if player_id in id_store or player_id not in new_cache[event_id].keys(): #why wouldn't it be in the data_cache?
                    continue
                else:
                    id_store.append(player_id)
                
                player_dict = dict(zip(col_names, player['Values']))
                
                for key, value in player_dict.items():
                    if key in new_cache[event_id][player_id].keys():
                        new_cache[event_id][player_id]['{}_{}'.format(key, i)] = value                 
                    else:
                        new_cache[event_id][player_id][key] = value
                        
        return new_cache
                    
                
    def _linestarapp_ownership_data(self, data_cache, json_data):
        new_cache = data_cache.copy()
        event_id = json_data['Ownership']['PeriodId']
        
        proj_key = list(json_data['Ownership']['Projected'].keys())[0]

        for player_id in new_cache[event_id].keys():
            for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
                new_cache[event_id][player_id][key] = None
        
        for player in json_data['Ownership']['Projected'][proj_key]:
            player_id = player['PlayerId']
            new_cache[event_id][player_id]['SalaryId'] = player['SalaryId']
            new_cache[event_id][player_id]['Owned'] = player['Owned']
        
        for player_id in new_cache[event_id].keys():
            if new_cache[event_id][player_id]['SalaryId']:
                salary_id = new_cache[event_id][player_id]['SalaryId']
                for player in json_data['AvgAdjustments']:
                    if salary_id == player['SalaryId']:
                        for key in ['HateCount', 'LoveCount']:
                            new_cache[event_id][player_id][key] = player[key]
                        
        return new_cache


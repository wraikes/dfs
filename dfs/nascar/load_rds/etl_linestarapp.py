import boto3
import json
import pandas as pd
import configparser
import psycopg2

from sql_queries import *

class LinestarappETL:
    def __init__(self, cursor):
        self.cursor = cursor


    def transform_linestarapp(self, json_data):
        data_cache = {}
        
        data_cache = self._linestarapp_salary_data(data_cache, json_data)
        data_cache = self._linestarapp_matchup_data(data_cache, json_data)
        data_cache = self._linestarapp_ownership_data(data_cache, json_data)
    
        return data_cache
    

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
        

    def insert_linestarapp(self, data, race_id):
        self.cursor.execute(nascar_linestarapp_insert,
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
    

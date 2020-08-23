import boto3
import re
import json
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime

#from database_connection.database_connection import connect_to_database


class ProcessData:

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    def __init__(self, sport):
        self.sport = sport
        self.cache_pids = []
        self.raw_data = {
            'fd': [],
            'dk': []
        }

    def get_cache_pids(self):
        #load cache
        self.cache_pids = cache[sport]

    def s3_pull(self):
        #pull data s3
        for obj in self.bucket.objects.filter(Prefix=self.sport):
            if 'json' in obj.key and 'linestarapp' in obj.key:
                pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
                site = obj.key.split('/')[-1].split('_')[0]

                if pid not in self.cache_pids:
                    data = self.extract(obj.key)
                    self.raw_data[site].append(data)

            elif 'sportsline' in obj.key:
                pass

    def extract(self, key):
        #extract the data and load in cache
        projections = True if 'projections' in key else False
        file = self.s3.Object('my-dfs-data', key)
        data = file.get()['Body'].read()
        data = json.loads(data)     
        data['projections'] = projections
        
        return data

    def transform_linestarapp(json_data):
        
        #loop through dict/list and transform each dict
        data_cache = {}
        
        for key in json_data.keys():
            
            data_cache[key] = []
            
            for data in json_data[key]:
                new_data = {}
                new_data = _linestarapp_salary_data(new_data, data)
                new_data = _linestarapp_matchup_data(new_data, data)
                new_data = _linestarapp_ownership_data(new_data, data)
                
                pid = list(new_data.keys())[0]
                for player in new_data[pid].keys():
                    new_data[pid][player]['projections'] = data['projections']
            
                data_cache[key].append(new_data)

        return data_cache


    def _linestarapp_salary_data(data_cache, json_data):
        new_cache = data_cache.copy()
        event_id = json_data['Ownership']['PeriodId']
        new_cache[event_id] = {}
        
        for player_data in json_data['Ownership']['Salaries']:
            player_id = player_data['PID']
            player_data['GT'] = datetime.strptime(player_data['GT'].split('T')[0], '%Y-%m-%d')
            new_cache[event_id][player_id] = player_data
        
        return new_cache


    def _linestarapp_matchup_data(data_cache, json_data):
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
                    new_cache[event_id][player_id]['{}_{}'.format(key, i)] = value
                        
        return new_cache
                    
                
    def _linestarapp_ownership_data(data_cache, json_data):
        new_cache = data_cache.copy()
        event_id = json_data['Ownership']['PeriodId']

        try:
            # proj_key = list(json_data['Ownership']['Projected'].keys())[0]

            for player_id in new_cache[event_id].keys():
                for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
                    new_cache[event_id][player_id][key] = None
            
            # for player_id in new_cache[event_id].keys():
            #     player_id = player['PlayerId']
            #     new_cache[event_id][player_id]['SalaryId'] = player['SalaryId']
            #     new_cache[event_id][player_id]['Owned'] = player['Owned']

            for player_id in new_cache[event_id].keys():
                salary_id = new_cache[event_id][player_id]['Id']
                
                for player in json_data['AvgAdjustments']:
                    if salary_id == player['SalaryId']:
                        for key in ['HateCount', 'LoveCount']:
                            new_cache[event_id][player_id][key] = player[key]
                    

        # #FD pid have no ownership data: 121, 157-164 
        # try:
        #     proj_key = list(json_data['Ownership']['Projected'].keys())[0]
        
        #     for player_id in new_cache[event_id].keys():
        #         for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
        #             new_cache[event_id][player_id][key] = None
            
        #     for player in json_data['Ownership']['Projected'][proj_key]:
        #         player_id = player['PlayerId']
        #         new_cache[event_id][player_id]['SalaryId'] = player['SalaryId']
        #         new_cache[event_id][player_id]['Owned'] = player['Owned']
            
        #     for player_id in new_cache[event_id].keys():
        #         if new_cache[event_id][player_id]['SalaryId']:
        #             salary_id = new_cache[event_id][player_id]['SalaryId']
        #             for player in json_data['AvgAdjustments']:
        #                 if salary_id == player['SalaryId']:
        #                     for key in ['HateCount', 'LoveCount']:
        #                         new_cache[event_id][player_id][key] = player[key]

        except:
            pass
                        
        return new_cache

    def connect_to_database(self):
        pass

    def load(self):
        #store pids in cache
        pass



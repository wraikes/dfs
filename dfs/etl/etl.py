#### add LOGs; player_id's not in ownership-salaries (id: 308 baddelley); event_id's missing data (fd: 121)

import boto3
import re
import json
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime

from database_connection.database_connection import connect_to_database
from etl.variables import get_variables
from etl.sql_queries import *

class LinestarappETL:
    '''
    The ETL process pulls data from designated s3 bucket, transforms it into
    a dictionary, and loads data into the proper postgres table
    '''
    _s3 = boto3.resource('s3')
    _bucket = _s3.Bucket('my-dfs-data') 


    def __init__(self, sport):
        self.sport = sport
        
        self._cache = {}
        self._data = {}


    #add decorator for connect_to_database()
    def extract(self):
        '''Pull data from s3 if PID is not already recorded in database,
        store in temporary cache based on fd or dk'''
        for site in ['fd', 'dk']:
            self._cache[site] = []
            
            #pid's used to append new data
            with connect_to_database() as cur:
                cur.execute('SELECT event_id FROM {}_linestarapp_{}'.format(self.sport, site))
                pids = set(x[0] for x in cur.fetchall())
    
            #loop thru bucket and extract data
            for obj in self._bucket.objects.filter(Prefix='{}/linestarapp/{}_'.format(self.sport, site)):
            
                #skip objects if folder or projection data
                if obj.key[-1] == '/':
                    continue
                
                #check if object is projection
                projections = True if 'projections' in obj.key else False
                
                #if file pid not in rds pid keys or file is projections, pull file, else continue        
                pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
                
                if pid in pids and not projections:
                    continue
                
                else:
                    file = self._s3.Object('my-dfs-data', obj.key)
                    data = file.get()['Body'].read()
                    data = json.loads(data)     
                    data['projections'] = projections
                    self._cache[site].append(data)


    def transform(self):
        '''Transforms the raw data in the _cache attribute into a more usable
        dictionary.'''
        for site in self._cache.keys():
            self._data[site] = {}
            
            for data in self._cache[site]:
                self._transform_salary_data(site, data)
                self._transform_matchup_data(site, data)
                self._transform_ownership_data(site, data)
                self._append_projections(site, data)

    
    def _transform_salary_data(self, site, record):
        event_id = record['Ownership']['PeriodId']
        self._data[site][event_id] = {}
        
        for player_data in record['Ownership']['Salaries']:
            player_id = player_data['PID']
            player_data['GT'] = datetime.strptime(player_data['GT'].split('T')[0], '%Y-%m-%d')
            self._data[site][event_id][player_id] = player_data
            
            for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
                self._data[site][event_id][player_id][key] = None


    def _transform_matchup_data(self, site, record):
        #note: player_id might not be in self._data[event_id], idk why.
        event_id = record['Ownership']['PeriodId']
      
        for i, table in enumerate(record['MatchupData']):
            col_names = table['Columns']
            id_cache = []
            
            for player_data in table['PlayerMatchups']:
                player_id = player_data['PlayerId']
                
                #sometimes player_data is duplicated or not included in ownership-salary data
                #### LOG THIS DATA
                if player_id in id_cache or player_id not in self._data[site][event_id].keys():
                    continue
                else:
                    id_cache.append(player_id)
                
                player_dict = dict(zip(col_names, player_data['Values']))
                
                for key, value in player_dict.items():
                    self._data[site][event_id][player_id]['{}_{}'.format(key, i)] = value
                        

    def _transform_ownership_data(self, site, record):
        #try/except might not to be incorporated
        
        event_id = record['Ownership']['PeriodId']
    
        for player_id in self._data[site][event_id].keys():
            salary_id = self._data[site][event_id][player_id]['Id']

            for player_data in record['AvgAdjustments']:
                if salary_id == player_data['SalaryId']:
                    for key in ['HateCount', 'LoveCount']:
                        self._data[site][event_id][player_id][key] = player_data[key]            
    
    
    def _append_projections(self, site, record):
        event_id = record['Ownership']['PeriodId']
        projection = record['projections']
        
        for player_id in self._data[site][event_id]:
            self._data[site][event_id][player_id]['projections'] = projection
        
        
    def load(self):
        var_keys, var_col_names = get_variables(self.sport)
        places = ('%s, ' * (len(var_keys)+1))[:-2]
        var_col_names = 'event_id, ' + var_col_names
        
        with connect_to_database() as cur:
            for site in self._data.keys():
                cur.execute(query_delete_projections.format(self.sport, site))
                
                for event_id in self._data[site]:
                    tmp_data = self._data[site][event_id]
                    
                    for player_id in tmp_data.keys():
                        values = (event_id, ) + tuple([
                            tmp_data[player_id][x] if tmp_data[player_id][x] != '-' else None for x in var_keys
                        ])
    
                        cur.execute(
                            query_insert_linestarapp.format(self.sport, site, var_col_names, places),
                            values
                        )


class SportslineETL:

    def extract_sportsline(self):
        pass
        
        # links = []
        # cols = ['link_pro', 'link_lead', 'link_bet']
        # tables = [
        #     '{}_sportsline_pro',
        #     '{}_sportsline_lead',
        #     '{}_sportsline_bet'
        # ]
        
        # #pid's used to append new data
        # with connect_to_database() as cur:
        #     for col, table in zip(cols, tables):
        #         cur.execute('SELECT DISTINCT {} FROM {}'.format(col, table))
        #         [links.append(link[0]) for link in cur.fetchall()]
        
        # #loop thru bucket and extract data
        # for obj in bucket.objects.filter(Prefix='{}/{}/'.format(sport, 'sportsline')):
        #     #skip objects if folder
        #     if obj.key[-1] == '/':
        #         continue
            
        #     #if file pid not in rds pid keys, pull file, else continue        
        #     link = obj.key.split('/')[-1]
            
        #     if link in links:
        #         continue
        #     else:
        #         file = s3.Object('my-dfs-data', obj.key)
        #         data = file.get()['Body'].read()
        #         data = json.loads(data)
    
        #     # if 'dfs-pro' in link:
        #     #     data = _transform_sportsline_pro(data, link)
        #     #     for row in data:
        #     #         _insert_sportsline_pro(row)
                    
        #     # elif 'surprising-picks' in link and sport == 'pga': 
        #     #     data = _extract_sportsline_lead(data)
        #     #     data = _transform_sportsline_lead(data, link)
        #     #     for row in data:
        #     #         _insert_sportsline_lead(row)
            
        #     ### have to think about how different titles relate to different sports
    
    # def transform_sportsline_lead(file):
    #     try:
    #         cache = {}
        
    #         cache['title'] = file['details']['title']
    #         cache['date'] = file['details']['content_date']
    #         cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
            
    #         tmp_cache = file['metaData']['body'].split('10:</strong></p>')
    #         if '<br>' in tmp_cache[1]:
    #             positions = tmp_cache[1].split('<br>')
            
    #         positions = _clean_positions_picks(positions)
        
    #         for i, pos in enumerate(positions):
    #             cache['pos_{}'.format(i+1)] = pos[0].strip()
                
    #         return cache
        
    #     except:
    #         return {}


    # def _clean_positions_picks(positions):
    #     new = []
    #     for pos in positions:
    #         pos = pos.replace('\t', '').replace('/', '-')
    #         pos = re.sub(r'\<.+\>', ' ', pos)
    #         pos_ = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
    #         pos_odds = re.findall(r'\d+-\d+', pos)
    #         pos_ += pos_odds
    #         if pos_:
    #             new.append(pos_)
    #     return new
        
    
    
    
    
    # def _clean_positions_dfs_pro(positions, dk):
    #     new = []
    #     for pos in positions:
    #         pos = pos.replace('D\t', '').replace('\t', '')
    #         pos = re.sub(r'\<.+\>', '', pos)
    #         pos = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
    #         if pos:
    #             new.append(pos)
                
    #     if not dk:
    #         new = new[5:] + new[0:5]
        
    #     return new
    
    
    # def _sportsline_dfs_pro_data(file):
    #     try: 
    #         cache = {}
    #         positions = []
    #         dk = True
            
    #         cache['title'] = file['details']['title']
    #         cache['date'] = file['details']['content_date']
    #         cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
            
    #         text = file['details']['body']
            
    #         if '<strong>DraftKings' in text:
    #             if '<strong>FanDuel' in text:
    #                 if text.find('<strong>FanDuel') > text.find('<strong>DraftKings'):
    #                     tmp_cache = text.split('<strong>DraftKings')[1].split('<strong>FanDuel')
    #                 else:
    #                     dk = False
    #                     tmp_cache = text.split('<strong>FanDuel')[1].split('<strong>DraftKings')
    #             else:
    #                 tmp_cache = [text.split('<strong>DraftKings')[1]]
    #         else:
    #             tmp_cache = text.split('</strong></p><p>')[1:]
    #         if '<br>' in tmp_cache[0]:
    #             positions += tmp_cache[0].split('<br>')
    #         else:
    #             positions += tmp_cache[0].split('</p><p>')
    #         if len(tmp_cache) > 1:
    #             if '<br>' in tmp_cache[1]:
    #                 positions += tmp_cache[1].split('<br>')
    #             else:
    #                 positions += tmp_cache[1].split('</p><p>')
        
    #         positions = _clean_positions_dfs_pro(positions, dk)
        
    #         for i, pos in enumerate(positions):
    #             cache['pos_{}'.format(i+1)] = pos[0].strip()
        
    #         return cache
            
    #     except:
    #         return {}







class FantasyNerdETL:
            
    def extract_fantasynerd(self):
        pass


import boto3
import re
import json
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime

from database_connection.database_connection import connect_to_database


class LinearstarappData:

    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.bucket = s3.Bucket('my-dfs-data') 
         
        self.sites = ['fd', 'dk']
        self.raw_files = {}
        self.processed_files = {}

        self.tmp_data = {}
        self.event_id = None

    def extract(self, sport):
    
        for site in self.sites:
            self.raw_files[site] = []
            
            #pid's used to append new data
            with connect_to_database() as cur:
                cur.execute('SELECT event_id FROM {}_linestarapp_{}'.format(sport, site))
                pids = set(x[0] for x in cur.fetchall())
    
            #loop thru bucket and extract data
            for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format(sport, 'linestarapp', site)):
            
                #skip objects if folder or projection data
                if obj.key[-1] == '/':
                    continue
                
                #check if object is projection
                projections = True if 'projections' in obj.key else False
                
                #if file pid not in rds pid keys or file is projections, pull file, else continue        
                pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
                
                if pid not in pids or projections:
                    file = s3.Object('my-dfs-data', obj.key)
                    data = file.get()['Body'].read()
                    data = json.loads(data)     
                    data['projections'] = projections
                    self.raw_files[site].append(data)
                else:
                    continue

    
    def transform(self):
        
        #loop through dict/list and transform each dict
        for key in self.sites:
             
            self.processed_files[key] = []
             
            for data in self.raw_files[key]:
                _transform_salary_data(data, key)
                _transform_matchup_data(data, key)
                _transform_ownership_data(data, key)
                


                pid = list(self.tmp_data.keys())[0]
                for player in self.tmp_data[pid].keys():
                    self.tmp_data[pid][player]['projections'] = data['projections']
            
                self.processed_files[key].append(self.tmp_data)


    def _transform_salary_data(json_data, key):
        self.event_id = json_data['Ownership']['PeriodId']
        self.tmp_data = {}
        self.tmp_data[self.event_id] = {}
        
        for player_data in json_data['Ownership']['Salaries']:
            player_id = player_data['PID']
            player_data['GT'] = datetime.strptime(player_data['GT'].split('T')[0], '%Y-%m-%d')
            self.tmp_data[self.event_id][player_id] = player_data
    
    
    def _linestarapp_matchup_data(json_data, key):
      
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
                    self.tmp_data[self.event_id][player_id]['{}_{}'.format(key, i)] = value
                        
                
def _linestarapp_ownership_data(json_data, key):

    try:

        for player_id in self.tmp_data[self.event_id].keys():
            for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
                self.tmp_data[self.event_id][player_id][key] = None
        
        for player_id in self.tmp_data[self.event_id].keys():
            salary_id = self.tmp_data[self.event_id][player_id]['Id']
            
            for player in json_data['AvgAdjustments']:
                if salary_id == player['SalaryId']:
                    for key in ['HateCount', 'LoveCount']:
                        self.tmp_data[self.event_id][player_id][key] = player[key]
                
    except:
        pass
                    






def transform_sportsline_lead(file):
    try:
        cache = {}
    
        cache['title'] = file['details']['title']
        cache['date'] = file['details']['content_date']
        cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
        
        tmp_cache = file['metaData']['body'].split('10:</strong></p>')
        if '<br>' in tmp_cache[1]:
            positions = tmp_cache[1].split('<br>')
        
        positions = _clean_positions_picks(positions)
    
        for i, pos in enumerate(positions):
            cache['pos_{}'.format(i+1)] = pos[0].strip()
            
        return cache
    
    except:
        return {}






def _clean_positions_picks(positions):
    new = []
    for pos in positions:
        pos = pos.replace('\t', '').replace('/', '-')
        pos = re.sub(r'\<.+\>', ' ', pos)
        pos_ = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
        pos_odds = re.findall(r'\d+-\d+', pos)
        pos_ += pos_odds
        if pos_:
            new.append(pos_)
    return new
    




def _clean_positions_dfs_pro(positions, dk):
    new = []
    for pos in positions:
        pos = pos.replace('D\t', '').replace('\t', '')
        pos = re.sub(r'\<.+\>', '', pos)
        pos = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
        if pos:
            new.append(pos)
            
    if not dk:
        new = new[5:] + new[0:5]
    
    return new


def _sportsline_dfs_pro_data(file):
    try: 
        cache = {}
        positions = []
        dk = True
        
        cache['title'] = file['details']['title']
        cache['date'] = file['details']['content_date']
        cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
        
        text = file['details']['body']
        
        if '<strong>DraftKings' in text:
            if '<strong>FanDuel' in text:
                if text.find('<strong>FanDuel') > text.find('<strong>DraftKings'):
                    tmp_cache = text.split('<strong>DraftKings')[1].split('<strong>FanDuel')
                else:
                    dk = False
                    tmp_cache = text.split('<strong>FanDuel')[1].split('<strong>DraftKings')
            else:
                tmp_cache = [text.split('<strong>DraftKings')[1]]
        else:
            tmp_cache = text.split('</strong></p><p>')[1:]
        if '<br>' in tmp_cache[0]:
            positions += tmp_cache[0].split('<br>')
        else:
            positions += tmp_cache[0].split('</p><p>')
        if len(tmp_cache) > 1:
            if '<br>' in tmp_cache[1]:
                positions += tmp_cache[1].split('<br>')
            else:
                positions += tmp_cache[1].split('</p><p>')
    
        positions = _clean_positions_dfs_pro(positions, dk)
    
        for i, pos in enumerate(positions):
            cache['pos_{}'.format(i+1)] = pos[0].strip()
    
        return cache
        
    except:
        return {}



















        
        
        
        
# def transform_sportsline_picks(data, link):
#     new_data = []
    
#     for key in data.keys():
#         tmp = {}
        
#         if 'pos_' in key:
#             pos = key.split('_')[1]
#             tmp['link_picks'] = link
#             tmp['title_picks'] = data['title']
#             tmp['date_picks'] = data['date']
#             tmp['name'] = data[key]
#             tmp['pos_picks'] = pos
            
#             new_data.append(tmp)
    
#     return new_data


# def transform_sportsline_dfs_pro(data, link):
#     new_data = []

#     for key in data.keys():
#         tmp = {}

#         if 'pos_' in key:
#             pos = int(key.split('_')[1])
#             if pos < 7: #only look at draftkings
#                 tmp['link_pro'] = link
#                 tmp['title_pro'] = data['title']
#                 tmp['date_pro'] = data['date']
#                 tmp['name'] = data[key]
#                 tmp['dfs_pick_dk'] = 1 
    
#                 new_data.append(tmp)

#     return new_data




















def etl_sportsline(sport):
    #initialize bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    data_files = {}
    
    links = []
    cols = ['link_pro', 'link_lead', 'link_bet']
    tables = [
        '{}_sportsline_pro',
        '{}_sportsline_lead',
        '{}_sportsline_bet'
    ]
    
    #pid's used to append new data
    with connect_to_database() as cur:
        for col, table in zip(cols, tables):
            cur.execute('SELECT DISTINCT {} FROM {}'.format(col, table))
            [links.append(link[0]) for link in cur.fetchall()]
    
    #loop thru bucket and extract data
    for obj in bucket.objects.filter(Prefix='{}/{}/'.format(sport, 'sportsline')):
        #skip objects if folder
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

        # if 'dfs-pro' in link:
        #     data = _transform_sportsline_pro(data, link)
        #     for row in data:
        #         _insert_sportsline_pro(row)
                
        # elif 'surprising-picks' in link and sport == 'pga': 
        #     data = _extract_sportsline_lead(data)
        #     data = _transform_sportsline_lead(data, link)
        #     for row in data:
        #         _insert_sportsline_lead(row)
        
        ### have to think about how different titles relate to different sports

        



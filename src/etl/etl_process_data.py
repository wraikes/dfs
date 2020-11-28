import boto3
import re
import json
import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO


class LinestarETL:

    def __init__(self, sport, projections):
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket('my-dfs-data') 
        
        self.sport = sport
        self.projections = projections

        self.sites = ['fd', 'dk']
        self.raw_files = {}
        self.processed_files = {}
        self.final_df = {}

        self.folder = f'{self.sport}/linestarapp/'
        self.folder_projections = f'{self.sport}/modeling/projections/'
        self.data_save = f'{self.sport}/modeling/data_'
        self.data_save_projections = f'{self.sport}/modeling/projections_data_'

        #temp cache for updating records
        self.tmp_data = {}
        self.event_id = None


    def extract(self):
    
        for site in self.sites:
            self.raw_files[site] = []
    
            #loop thru bucket and extract data
            prefix = self.folder_projections if self.projections else self.folder

            for obj in self.bucket.objects.filter(Prefix=f'{prefix}{site}'):
            
                #skip objects if folder or projection data
                if obj.key[-1] == '/':
                    continue
                
                file = self.s3.Object('my-dfs-data', obj.key)
                data = file.get()['Body'].read()
                data = json.loads(data)     
                self.raw_files[site].append(data)

    
    def transform(self):
        
        #loop through dict/list and transform each dict
        for site in self.sites:
             
            self.processed_files[site] = []
             
            for data in self.raw_files[site]:
                self._transform_salary_data(data)
                self._transform_matchup_data(data)
                self._transform_updates(data)
                
                self.processed_files[site].append(self.tmp_data)


    def _transform_salary_data(self, json_data):
        self.event_id = json_data['Ownership']['PeriodId']
        self.tmp_data = {}
        self.tmp_data[self.event_id] = {}
        
        for player_data in json_data['Ownership']['Salaries']:
            player_id = player_data['PID']
            player_data['GT'] = datetime.strptime(player_data['GT'].split('T')[0], '%Y-%m-%d')
            self.tmp_data[self.event_id][player_id] = player_data
    
    
    def _transform_matchup_data(self, json_data):
      
        for i, table in enumerate(json_data['MatchupData']):
            col_names = table['Columns']
            id_store = []
            
            for player in table['PlayerMatchups']:
                player_id = player['PlayerId']
    
                #this avoids duplicates
                if player_id in id_store or player_id not in self.tmp_data[self.event_id].keys():
                    continue
                else:
                    id_store.append(player_id)
                
                player_dict = dict(zip(col_names, player['Values']))
                
                for key, value in player_dict.items():
                    self.tmp_data[self.event_id][player_id][f'{key}_{i}'] = value


    def _transform_updates(self, json_data):
        salaryid_cache = []

        updates = json.loads(json_data['SalaryContainerJson'])
        for update in updates['SalariesMap']['Variants']:

            salaryid = update['psid']
            pp = update['sp']
            sal = update['s']
            pid = None

            if salaryid in salaryid_cache:
                continue
                
            for player_id in self.tmp_data[self.event_id].keys():
                idx = self.tmp_data[self.event_id][player_id]['Id']

                if salaryid == self.tmp_data[self.event_id][player_id]['Id']:
                    pid = player_id
                    salaryid_cache.append(salaryid)
            if pid:
                self.tmp_data[self.event_id][pid]['PP'] = pp
                self.tmp_data[self.event_id][pid]['SAL'] = sal


    def load(self):

        for site in self.sites:
            df = pd.DataFrame()

            for data in self.processed_files[site]:
                tmp_df = pd.DataFrame.from_dict(
                    {(i,j): data[i][j] for i in data.keys() for j in data[i].keys()},
                    orient='index'
                )

                df = df.append(tmp_df)
            
            cols = list(df.columns)
            df = df.reset_index()
            df.columns = ['event_id', 'player_id'] + cols
            self.final_df[site] = df.copy()

            #save df to bucket
            data_save = self.data_save_projections if self.projections else self.data_save
            
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            self.s3.Object(self.bucket.name, f'{data_save}{site}.csv').put(Body=csv_buffer.getvalue())



                
    # def _transform_ownership_data(json_data, key):

    #     for player_id in self.tmp_data[self.event_id].keys():
    #         for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
    #             self.tmp_data[self.event_id][player_id][key] = None
        
    #     for player_id in self.tmp_data[self.event_id].keys():
    #         salary_id = self.tmp_data[self.event_id][player_id]['Id']
            
    #         for player in json_data['AvgAdjustments']:
    #             if salary_id == player['SalaryId']:
    #                 for key in ['HateCount', 'LoveCount']:
    #                     self.tmp_data[self.event_id][player_id][key] = player[key]
                    

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





















#    def _linestarapp_ownership_data(json_data, key):
#    
#        try:
#    
#            for player_id in self.tmp_data[self.event_id].keys():
#                for key in ['SalaryId', 'Owned', 'HateCount', 'LoveCount']:
#                    self.tmp_data[self.event_id][player_id][key] = None
#            
#            for player_id in self.tmp_data[self.event_id].keys():
#                salary_id = self.tmp_data[self.event_id][player_id]['Id']
#                
#                for player in json_data['AvgAdjustments']:
#                    if salary_id == player['SalaryId']:
#                        for key in ['HateCount', 'LoveCount']:
#                            self.tmp_data[self.event_id][player_id][key] = player[key]
#                    
#        except:
#            pass
#                        

#
#
#
#
#def transform_sportsline_lead(file):
#    try:
#        cache = {}
#    
#        cache['title'] = file['details']['title']
#        cache['date'] = file['details']['content_date']
#        cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
#        
#        tmp_cache = file['metaData']['body'].split('10:</strong></p>')
#        if '<br>' in tmp_cache[1]:
#            positions = tmp_cache[1].split('<br>')
#        
#        positions = _clean_positions_picks(positions)
#    
#        for i, pos in enumerate(positions):
#            cache['pos_{}'.format(i+1)] = pos[0].strip()
#            
#        return cache
#    
#    except:
#        return {}
#
#
#
#
#
#
#def _clean_positions_picks(positions):
#    new = []
#    for pos in positions:
#        pos = pos.replace('\t', '').replace('/', '-')
#        pos = re.sub(r'\<.+\>', ' ', pos)
#        pos_ = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
#        pos_odds = re.findall(r'\d+-\d+', pos)
#        pos_ += pos_odds
#        if pos_:
#            new.append(pos_)
#    return new
#    
#
#
#
#
#def _clean_positions_dfs_pro(positions, dk):
#    new = []
#    for pos in positions:
#        pos = pos.replace('D\t', '').replace('\t', '')
#        pos = re.sub(r'\<.+\>', '', pos)
#        pos = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
#        if pos:
#            new.append(pos)
#            
#    if not dk:
#        new = new[5:] + new[0:5]
#    
#    return new
#
#
#def _sportsline_dfs_pro_data(file):
#    try: 
#        cache = {}
#        positions = []
#        dk = True
#        
#        cache['title'] = file['details']['title']
#        cache['date'] = file['details']['content_date']
#        cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
#        
#        text = file['details']['body']
#        
#        if '<strong>DraftKings' in text:
#            if '<strong>FanDuel' in text:
#                if text.find('<strong>FanDuel') > text.find('<strong>DraftKings'):
#                    tmp_cache = text.split('<strong>DraftKings')[1].split('<strong>FanDuel')
#                else:
#                    dk = False
#                    tmp_cache = text.split('<strong>FanDuel')[1].split('<strong>DraftKings')
#            else:
#                tmp_cache = [text.split('<strong>DraftKings')[1]]
#        else:
#            tmp_cache = text.split('</strong></p><p>')[1:]
#        if '<br>' in tmp_cache[0]:
#            positions += tmp_cache[0].split('<br>')
#        else:
#            positions += tmp_cache[0].split('</p><p>')
#        if len(tmp_cache) > 1:
#            if '<br>' in tmp_cache[1]:
#                positions += tmp_cache[1].split('<br>')
#            else:
#                positions += tmp_cache[1].split('</p><p>')
#    
#        positions = _clean_positions_dfs_pro(positions, dk)
#    
#        for i, pos in enumerate(positions):
#            cache['pos_{}'.format(i+1)] = pos[0].strip()
#    
#        return cache
#        
#    except:
#        return {}






        
        
        
        
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




#
#def etl_sportsline(sport):
#    #initialize bucket
#    s3 = boto3.resource('s3')
#    bucket = s3.Bucket('my-dfs-data')
#    data_files = {}
#    
#    links = []
#    cols = ['link_pro', 'link_lead', 'link_bet']
#    tables = [
#        '{}_sportsline_pro',
#        '{}_sportsline_lead',
#        '{}_sportsline_bet'
#    ]
#    
#    #pid's used to append new data
#    with connect_to_database() as cur:
#        for col, table in zip(cols, tables):
#            cur.execute('SELECT DISTINCT {} FROM {}'.format(col, table))
#            [links.append(link[0]) for link in cur.fetchall()]
#    
#    #loop thru bucket and extract data
#    for obj in bucket.objects.filter(Prefix='{}/{}/'.format(sport, 'sportsline')):
#        #skip objects if folder
#        if obj.key[-1] == '/':
#            continue
#        
#        #if file pid not in rds pid keys, pull file, else continue        
#        link = obj.key.split('/')[-1]
#        
#        if link in links:
#            continue
#        else:
#            file = s3.Object('my-dfs-data', obj.key)
#            data = file.get()['Body'].read()
#            data = json.loads(data)
#
#        # if 'dfs-pro' in link:
#        #     data = _transform_sportsline_pro(data, link)
#        #     for row in data:
#        #         _insert_sportsline_pro(row)
#                
#        # elif 'surprising-picks' in link and sport == 'pga': 
#        #     data = _extract_sportsline_lead(data)
#        #     data = _transform_sportsline_lead(data, link)
#        #     for row in data:
#        #         _insert_sportsline_lead(row)
#        
#        ### have to think about how different titles relate to different sports
#
#        
#

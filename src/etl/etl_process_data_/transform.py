import pandas as pd
import psycopg2
import configparser
import boto3
import numpy as np
from datetime import datetime


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
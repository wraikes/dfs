import boto3
import re
import json
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime

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
    

def _sportsline_picks_data(file):
    try:
        cache = {}
    
        cache['title'] = file['details']['title']
        cache['date'] = file['details']['content_date']
        cache['date'] = datetime.fromtimestamp(file['details']['content_date'])
        
        tmp_cache = file['metaData']['body'].split('10:</strong></p>')
        if '<br>' in tmp_cache[1]:
            positions = tmp_cache[1].split('<br>')
    
        # if len(positions) < 21:
        #     if len(tmp_cache) > 2:
        #         if '</p><p>' in tmp_cache[2]:
        #             positions += tmp_cache[2].split('</p><p>')
        #         else:
        #             positions += tmp_cache[2].split('<br>')
        
        #         if '<br>' in tmp_cache[1]:
        #             positions = tmp_cache[1].split('<br>')
        #         else:
        #             positions = tmp_cache[1].split('</li><li>')
        #         if len(tmp_cache) > 2:
        #             positions += tmp_cache[2].split('<br>')
                
        # if len(positions) < 21:
        #     positions = [x.split('<br>')[0] for x in file['metaData']['body'].split('\t')[1:]]
        
        positions = _clean_positions_picks(positions)
    
        for i, pos in enumerate(positions):
            cache['pos_{}'.format(i+1)] = pos[0].strip()
            
        return cache
    
    except:
        return {}


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
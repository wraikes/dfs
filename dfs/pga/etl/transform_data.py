import pandas as pd
import psycopg2
import configparser
import boto3
import numpy as np


def transform_sportsline_picks(data, link):
    new_data = []
    
    for key in data.keys():
        tmp = {}
        
        if 'pos_' in key:
            pos = key.split('_')[1]
            tmp['link_picks'] = link
            tmp['title_picks'] = data['title']
            tmp['date_picks'] = data['date']
            tmp['name'] = data[key]
            tmp['pos_picks'] = pos
            
            new_data.append(tmp)
    
    return new_data


def transform_sportsline_dfs_pro(data, link):
    new_data = []

    for key in data.keys():
        tmp = {}

        if 'pos_' in key:
            pos = int(key.split('_')[1])
            if pos < 7: #only look at draftkings
                tmp['link_pro'] = link
                tmp['title_pro'] = data['title']
                tmp['date_pro'] = data['date']
                tmp['name'] = data[key]
                tmp['dfs_pick_dk'] = 1 
    
                new_data.append(tmp)

    return new_data

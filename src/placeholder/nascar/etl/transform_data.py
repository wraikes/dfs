import pandas as pd
import psycopg2
import configparser
import boto3
import numpy as np


def transform_sportsline_leaderboard(data, link):
    new_data = []
    
    for key in data.keys():
        tmp = {}
        
        if 'pos_' in key:
            pos = key.split('_')[1]
            tmp['link_leaderboard'] = link
            tmp['title_leaderboard'] = data['title']
            tmp['date_leaderboard'] = data['date']
            tmp['name'] = data[key]
            tmp['pos_leaderboard'] = pos
            
            new_data.append(tmp)
    
    return new_data


def transform_sportsline_betting(data, link):
    new_data = []

    for key in data.keys():
        tmp = {}
        
        if 'pos_' in key and 'odds' not in key:
            pos = key.split('_')[1]
            tmp['link_betting'] = link
            tmp['title_betting'] = data['title']
            tmp['date_betting'] = data['date']
            tmp['name'] = data[key]
            tmp['pos_betting'] = pos
            tmp['pos_odds_betting'] = odds(data[key+'_odds'])
            
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


def odds(odds):
    if odds:
        tmp = [int(x) for x in odds.split('-')]
        tmp = tmp[1] / sum(tmp)
    else:
        tmp = None
    return tmp

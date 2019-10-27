import boto3
import re
import json
import pandas as pd
import numpy as np
import psycopg2

from sql_queries import *

def _clean_positions_leaderboard(positions):
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

def _sportsline_leaderboard_data(file):
    cache = {}

    cache['title'] = file['details']['title']
    cache['date'] = file['details']['content_date']
    
    tmp_cache = file['metaData']['body'].split(':</strong></p>')
    if '<br>' in tmp_cache[1]:
        positions = tmp_cache[1].split('<br>')
    else:
        positions = tmp_cache[1].split('</li><li>')
    if len(tmp_cache) > 2:
        if '</p><p>' in tmp_cache[2]:
            positions += tmp_cache[2].split('</p><p>')
        else:
            positions += tmp_cache[2].split('<br>')
    
    if len(positions) < 21:
        positions = [x.split('<br>')[0] for x in data['metaData']['body'].split('\t')[1:]]
    
    positions = _clean_positions_leaderboard(positions)

    for i, pos in enumerate(positions):
        cache['pos_{}'.format(i+1)] = pos[0].strip()
        
    return cache


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
    cache = {}
    positions = []
    dk = True
    
    cache['title'] = file['details']['title']
    cache['date'] = file['details']['content_date']
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
    
    
def _sportsline_betting_data(file):
    cache = {}
    
    cache['title'] = file['details']['title']
    cache['date'] = file['details']['content_date']
    
    positions = [x.split(' -')[0].split('</str')[0] for x in file['details']['body'].split('#')[1:]]
    
    new_pos = []
    for pos in positions:
        pos = pos.replace('/', '-')
        pos = re.sub(r'/d+ ', '', pos)
        pos_ = re.findall(r'[A-Z]+[a-z.]*\s[A-Z][a-z.]+[A-Z]*[a-z.]*\s*[A-Z]*[a-z.]*', pos)
        pos_odds = re.findall(r'\d+-\d+', pos)
        pos_ += pos_odds
        if pos_:
            new_pos.append(pos_)
        
    for i, pos in enumerate(new_pos):
        cache['pos_{}'.format(i+1)] = pos[0].strip()
        cache['pos_{}_odds'.format(i+1)] = pos[-1]

    return cache
    
    
def _insert_sportsline_dfs_pro(cur, link, data):
    cur.execute(nascar_sportsline_dfs_pro_insert, (
        link,
        data['title'],
        data['date'],
        data['pos_1'] if 'pos_1' in data.keys() else None,
        data['pos_2'] if 'pos_2' in data.keys() else None,
        data['pos_3'] if 'pos_3' in data.keys() else None,
        data['pos_4'] if 'pos_4' in data.keys() else None,
        data['pos_5'] if 'pos_5' in data.keys() else None,
        data['pos_6'] if 'pos_6' in data.keys() else None,
        data['pos_7'] if 'pos_7' in data.keys() else None,
        data['pos_8'] if 'pos_8' in data.keys() else None,
        data['pos_9'] if 'pos_9' in data.keys() else None,
        data['pos_10'] if 'pos_10' in data.keys() else None,
        data['pos_11'] if 'pos_11' in data.keys() else None
        )
)


def _insert_sportsline_betting(cur, link, data):
    cur.execute(nascar_sportsline_betting_insert, (
        link,
        data['title'],
        data['date'],
        data['pos_1'] if 'pos_1' in data.keys() else None,
        data['pos_2'] if 'pos_2' in data.keys() else None,
        data['pos_3'] if 'pos_3' in data.keys() else None,
        data['pos_4'] if 'pos_4' in data.keys() else None,
        data['pos_5'] if 'pos_5' in data.keys() else None,
        data['pos_6'] if 'pos_6' in data.keys() else None,
        data['pos_7'] if 'pos_7' in data.keys() else None,
        data['pos_8'] if 'pos_8' in data.keys() else None,
        data['pos_9'] if 'pos_9' in data.keys() else None,
        data['pos_10'] if 'pos_10' in data.keys() else None,
        data['pos_11'] if 'pos_11' in data.keys() else None,
        data['pos_12'] if 'pos_12' in data.keys() else None,
        data['pos_13'] if 'pos_13' in data.keys() else None,
        data['pos_14'] if 'pos_14' in data.keys() else None,
        data['pos_15'] if 'pos_15' in data.keys() else None,
        data['pos_16'] if 'pos_16' in data.keys() else None,
        data['pos_17'] if 'pos_17' in data.keys() else None,
        data['pos_18'] if 'pos_18' in data.keys() else None,
        data['pos_19'] if 'pos_19' in data.keys() else None,
        data['pos_20'] if 'pos_20' in data.keys() else None,
        data['pos_1_odds'] if 'pos_1_odds' in data.keys() else None,
        data['pos_2_odds'] if 'pos_2_odds' in data.keys() else None,
        data['pos_3_odds'] if 'pos_3_odds' in data.keys() else None,
        data['pos_4_odds'] if 'pos_4_odds' in data.keys() else None,
        data['pos_5_odds'] if 'pos_5_odds' in data.keys() else None,
        data['pos_6_odds'] if 'pos_6_odds' in data.keys() else None,
        data['pos_7_odds'] if 'pos_7_odds' in data.keys() else None,
        data['pos_8_odds'] if 'pos_8_odds' in data.keys() else None,
        data['pos_9_odds'] if 'pos_9_odds' in data.keys() else None,
        data['pos_10_odds'] if 'pos_10_odds' in data.keys() else None,
        data['pos_11_odds'] if 'pos_11_odds' in data.keys() else None,
        data['pos_12_odds'] if 'pos_12_odds' in data.keys() else None,
        data['pos_13_odds'] if 'pos_13_odds' in data.keys() else None,
        data['pos_14_odds'] if 'pos_14_odds' in data.keys() else None,
        data['pos_15_odds'] if 'pos_15_odds' in data.keys() else None,
        data['pos_16_odds'] if 'pos_16_odds' in data.keys() else None,
        data['pos_17_odds'] if 'pos_17_odds' in data.keys() else None,
        data['pos_18_odds'] if 'pos_18_odds' in data.keys() else None,
        data['pos_19_odds'] if 'pos_19_odds' in data.keys() else None,
        data['pos_20_odds'] if 'pos_20_odds' in data.keys() else None
    )
)


def _insert_sportsline_leaderboard(cur, link, data):
    cur.execute(nascar_sportsline_leaderboard_insert, (
        link,
        data['title'],
        data['date'],
        data['pos_1'] if 'pos_1' in data.keys() else None,
        data['pos_2'] if 'pos_2' in data.keys() else None,
        data['pos_3'] if 'pos_3' in data.keys() else None,
        data['pos_4'] if 'pos_4' in data.keys() else None,
        data['pos_5'] if 'pos_5' in data.keys() else None,
        data['pos_6'] if 'pos_6' in data.keys() else None,
        data['pos_7'] if 'pos_7' in data.keys() else None,
        data['pos_8'] if 'pos_8' in data.keys() else None,
        data['pos_9'] if 'pos_9' in data.keys() else None,
        data['pos_10'] if 'pos_10' in data.keys() else None,
        data['pos_11'] if 'pos_11' in data.keys() else None,
        data['pos_12'] if 'pos_12' in data.keys() else None,
        data['pos_13'] if 'pos_13' in data.keys() else None,
        data['pos_14'] if 'pos_14' in data.keys() else None,
        data['pos_15'] if 'pos_15' in data.keys() else None,
        data['pos_16'] if 'pos_16' in data.keys() else None,
        data['pos_17'] if 'pos_17' in data.keys() else None,
        data['pos_18'] if 'pos_18' in data.keys() else None,
        data['pos_19'] if 'pos_19' in data.keys() else None,
        data['pos_20'] if 'pos_20' in data.keys() else None,
        data['pos_21'] if 'pos_21' in data.keys() else None,
        data['pos_22'] if 'pos_22' in data.keys() else None,
        data['pos_23'] if 'pos_23' in data.keys() else None,
        data['pos_24'] if 'pos_24' in data.keys() else None,
        data['pos_25'] if 'pos_25' in data.keys() else None,
        data['pos_26'] if 'pos_26' in data.keys() else None,
        data['pos_27'] if 'pos_27' in data.keys() else None,
        data['pos_28'] if 'pos_28' in data.keys() else None,
        data['pos_29'] if 'pos_29' in data.keys() else None,
        data['pos_30'] if 'pos_30' in data.keys() else None,
        data['pos_31'] if 'pos_31' in data.keys() else None,
        data['pos_32'] if 'pos_32' in data.keys() else None,
        data['pos_33'] if 'pos_33' in data.keys() else None,
        data['pos_34'] if 'pos_34' in data.keys() else None,
        data['pos_35'] if 'pos_35' in data.keys() else None,
        data['pos_36'] if 'pos_36' in data.keys() else None,
        data['pos_37'] if 'pos_37' in data.keys() else None,
        data['pos_38'] if 'pos_38' in data.keys() else None,
        data['pos_39'] if 'pos_39' in data.keys() else None,
        data['pos_40'] if 'pos_40' in data.keys() else None
    )
)


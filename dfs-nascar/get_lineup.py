import pandas as pd
import numpy as np
import configparser
import pickle
import json
import sys

from nascar_lineups.scrape_nascar_data import NascarDataPull
from nascar_lineups.optimizer import Optimizer
from nascar_lineups.nascar_spider import NascarSpider

pid = int(sys.argv[1])
cfg = configparser.ConfigParser()
cfg.read('tmp.ini')

label = eval(cfg['TABLEVARIABLES']['label'])
predictors = eval(cfg['TABLEVARIABLES']['predictors'])
non_numeric_cols = eval(cfg['TABLEVARIABLES']['non_numeric_cols'])

data = NascarDataPull(train=False, pid=pid)
data.pull_json_data()
data.extract_owner_data()
data.extract_table_data()
data.extract_adjustment_data()

with open('./nascar_lineups/projections.json', 'rb') as file:
    append_data = json.load(file)

for player in append_data:
    player_id = player['player_id']
    
    data._final_data[pid][player_id]['Owned'] = float(player['owned'][:-1])
    data._final_data[pid][player_id]['LoveCount'] = player['lovecount']
    data._final_data[pid][player_id]['HateCount'] = player['hatecount']

df = data._final_data.copy()
df = pd.DataFrame.from_dict(
    {(i, j): df[i][j] for i in df.keys() for j in df[i].keys()},
    orient='index'
)

def data_clean(df, non_numeric_cols, predictors, label):
    
    df = df[label+predictors].dropna() 
    
    for col in df.columns:
        if col not in non_numeric_cols:
            df[col] = pd.to_numeric(df[col])
    
    #df['_name'] = df['name']  
    df['race_date'] = pd.to_datetime(df['race_date']).dt.date  
    df = pd.get_dummies(df, columns=['restrictor_plate', 'surface'], drop_first=True)
    
    def notes_clean(row):
        if [i for i in eval(row) if 'Qualified' in i['Note']]:
            return int([i for i in eval(row) if 'Qualified' in i['Note']][0]['Note'].split(' ')[-3][:-2]) 
        else:
            return np.nan
    
    df['notes'] = df['notes'].apply(lambda x: notes_clean(x))
    df['notes'] = np.where(df['notes'].isnull(), 
                        df['qualifying_pos'], 
                            df['notes'])
    
    return df

df.columns = [
    's', 'pid', 'name', 'pos', 'salary', 'gid', 'gi', 'race_date', 
    'ppg', 'pp', 'ps', 'ss', 'stat', 'is_', 'notes', 'floor', 'ceil', 'conf', 'ptid', 'otid', 
    'htid', 'oe', 'opprank', 'opptotal', 'dspid', 'dgid', 'img', 'pteam', 'hteam', 'oteam', 
    'lock', 'id', 'races', 'wins', 'top_fives', 'top_tens', 'avg_finish', 
    'laps_led_race', 'fastest_laps_race', 'avg_pass_diff', 'quality_passes_race', 
    'fppg', 'practice_laps', 'practice_best_lap_time', 'practice_best_lap_speed', 
    'qualifying_pos', 'qualifying_best_lap_time', 'qualifying_best_lap_speed', 
    'laps', 'miles', 'surface', 'restrictor_plate', 'cautions_race', 'races_3', 
    'finished', 'wins_3', 'top_5s', 'top_10s', 'avg_place', 'races_4', 'finished_4', 
    'wins_4', 'top_5s_4', 'top_10s_4', 'avg_place_4', 'salaryid', 
    'owned', 'hatecount', 'lovecount'
]

df['qualifying_pos'] = np.where(df['qualifying_pos']=='-', 25, df['qualifying_pos'])
df = data_clean(df, non_numeric_cols, predictors, label)

# load model
with open('./nascar_model.pkl', 'rb') as file:
    model = pickle.load(file)

for col in model[1]:
    if col not in df.columns:
        df[col] = 0
        
df['preds'] = (model[0].predict(df[model[1]]) + df['fppg']) / 2

# get predictions
opt = Optimizer(df)
opt.solve()
opt.get_lineup()

print(opt.lineup)

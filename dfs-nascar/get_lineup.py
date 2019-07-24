import pandas as pd
import numpy as np
import configparser
import pickle
from nascar_lineups.scrape_nascar_data import NascarDataPull
from nascar_lineups.optimizer import Optimizer

cfg = configparser.ConfigParser()
cfg.read('tmp.ini')

label = eval(cfg['TABLEVARIABLES']['label'])
predictors = eval(cfg['TABLEVARIABLES']['predictors'])
non_numeric_cols = eval(cfg['TABLEVARIABLES']['non_numeric_cols'])

data = NascarDataPull(train=False, pid=258)
data.pull_json_data()
data.extract_owner_data()
data.extract_table_data()
data.extract_adjustment_data()

append_data = {258: {
    9: {
        'Owned': 26.25,
        'LoveCount': 3,
        'HateCount': 0 
    },
    34: {
        'Owned': 25,
        'LoveCount': 1,
        'HateCount': 0 
    },
    44: {
        'Owned': 24.8,
        'LoveCount': 2,
        'HateCount': 0 
    },
    15: {
        'Owned': 24.05,
        'LoveCount': 1,
        'HateCount': 0 
    },
    19: {
        'Owned': 22.05,
        'LoveCount': 1,
        'HateCount': 2 
    },
    14: {
        'Owned': 18,
        'LoveCount': 1,
        'HateCount': 0 
    },
    8: {
        'Owned': 27.95,
        'LoveCount': 1,
        'HateCount': 0 
    },
    102: {
        'Owned': 20.85,
        'LoveCount': 0,
        'HateCount': 0 
    },
    81: {
        'Owned': 19.05,
        'LoveCount': 1,
        'HateCount': 0 
    },
    86: {
        'Owned': 15.85,
        'LoveCount': 0,
        'HateCount': 0 
    },
    85: {
        'Owned': 19.55,
        'LoveCount': 0,
        'HateCount': 0 
    },
    16: {
        'Owned': 18.9,
        'LoveCount': 0,
        'HateCount': 0 
    },
    6: {
        'Owned': 16.2,
        'LoveCount': 0,
        'HateCount': 0 
    },
    104: {
        'Owned': 22.2,
        'LoveCount': 0,
        'HateCount': 0 
    },
    1: {
        'Owned': 20.7,
        'LoveCount': 0,
        'HateCount': 0 
    },
    141: {
        'Owned': 19.5,
        'LoveCount': 0,
        'HateCount': 0 
    },
    155: {
        'Owned': 17,
        'LoveCount': 1,
        'HateCount': 0 
    },
    28: {
        'Owned': 24.8,
        'LoveCount': 0,
        'HateCount': 0 
    },
    53: {
        'Owned': 13.65,
        'LoveCount': 0,
        'HateCount': 0 
    },
    57: {
        'Owned': 11.15,
        'LoveCount': 0,
        'HateCount': 1 
    },
    101: {
        'Owned': 21.4,
        'LoveCount': 1,
        'HateCount': 0 
    },
    26: {
        'Owned': 15.45,
        'LoveCount': 1,
        'HateCount': 0 
    },
    159: {
        'Owned': 9.15,
        'LoveCount': 0,
        'HateCount': 1 
    },
    99: {
        'Owned': 16,
        'LoveCount': 1,
        'HateCount': 1 
    },
    109: {
        'Owned': 6.45,
        'LoveCount': 0,
        'HateCount': 1 
    },
    91: {
        'Owned': 10.2,
        'LoveCount': 0,
        'HateCount': 1 
    },
    42: {
        'Owned': 10.05,
        'LoveCount': 0,
        'HateCount': 2
    },
    95: {
        'Owned': 4.95,
        'LoveCount': 0,
        'HateCount': 1 
    },
    29: {
        'Owned': 7.55,
        'LoveCount': 0,
        'HateCount': 1 
    },
    145: {
        'Owned': 8.65,
        'LoveCount': 0,
        'HateCount': 0 
    },
    167: {
        'Owned': 5.15,
        'LoveCount': 0,
        'HateCount': 0 
    },
    41: {
        'Owned': 2.3,
        'LoveCount': 0,
        'HateCount': 1 
    },
    144: {
        'Owned': 4,
        'LoveCount': 0,
        'HateCount': 2
    },
    31: {
        'Owned': 2.15,
        'LoveCount': 0,
        'HateCount': 1 
    },
    168: {
        'Owned': 2,
        'LoveCount': 0,
        'HateCount': 0 
    }
}}

for player in append_data[258].keys():
    data._final_data[258][player]['Owned'] = append_data[258][player]['Owned']
    data._final_data[258][player]['LoveCount'] = append_data[258][player]['LoveCount']
    data._final_data[258][player]['HateCount'] = append_data[258][player]['HateCount']

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
    'lovecount', 'hatecount', 'adj', 'owned'
]

df['qualifying_pos'] = np.where(df['qualifying_pos']=='-', 25, df['qualifying_pos'])
df = data_clean(df, non_numeric_cols, predictors, label)

# load model
with open('./nascar_model.pkl', 'rb') as file:
    model = pickle.load(file)

for col in model[1]:
    if col not in df.columns:
        df[col] = 0
        
df['preds'] = model[0].predict(df[model[1]])

# get predictions
opt = Optimizer(df)
opt.solve()
opt.get_lineup()

print(opt.lineup)

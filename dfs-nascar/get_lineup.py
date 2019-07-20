import pandas as pd
import configparser
from joblib import load
from ..scrape_nascar_data import NascarDataPull
from optimizer import Optimizer

cfg = configparser.ConfigParser()
cfg.read('build_model.ini')

label = eval(cfg['TABLEVARIABLES']['label'])
predictors = eval(cfg['TABLEVARIABLES']['predictors'])
non_numeric_cols = eval(cfg['TABLEVARIABLES']['non_numeric_cols'])

df = NascarDataPull(train=False, pid=258)
df.pull_json_data()
df.extract_owner_data()
df.extract_table_data()

df = df._final_data.copy()
df = pd.DataFrame.from_dict(
    {(i, j): df[i][j] for i in df.keys() for j in df[i].keys()},
    orient='index'
)

def data_clean(df, non_numeric_cols, predictors):
    
    df = df[predictors].dropna() 
    
    for col in df.columns:
        if col not in non_numeric_cols:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                print(col)
    
    return df


df = data_clean(df, non_numeric_cols, predictors)
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
    'wins_4', 'top_5s_4', 'top_10s_4', 'avg_place_4'
]

# load model
model = load('../get_model/nascar_model.joblib')
model.predict(df[predictors])

# get predictions
opt = Optimizer(df)
opt.solve()
opt.get_lineup()

print(opt.lineup)

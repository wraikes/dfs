import pandas as pd
import numpy as np

from ..nascar_lineups.load_data import LoadData
from ..nascar_lineups.optimizer import Optimizer
from ..nascar_lineups.build_model import Model

non_numeric_cols = ['race_date', 'name', 'restrictor_plate', 'surface']
label = ['ps']
predictors = [
    'name',
    'salary',
    'race_date',
    'pp',
    'races',
    'wins',
    'top_fives',
    'top_tens',
    'avg_finish',
    'laps_led_race',
    'fastest_laps_race',
    'avg_pass_diff',
    'quality_passes_race',
    'fppg',
    'practice_laps',
    'practice_best_lap_time',
    'practice_best_lap_speed',
    'qualifying_pos',
    'qualifying_best_lap_time',
    'qualifying_best_lap_speed',
    'laps',
    'miles',
    'surface',
    'restrictor_plate',
    'cautions_race',
    'races_3',
    'finished',
    'wins_3',
    'top_5s',
    'top_10s',
    'avg_place',
    'races_4',
    'finished_4',
    'wins_4',
    'top_5s_4',
    'top_10s_4',
    'avg_place_4'
]

load = LoadData('./tmp.ini', 'nascar_linestar')
load.setup_connection()
load.create_df()
df = load.data_clean(non_numeric_cols, predictors, label)

#from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
ridge = LinearRegression()
params = []
model = Model(ridge, params)

performance = {}
    
for date in df.race_date.sort_values().unique()[1:]:
    df_train = df[df.race_date < date].drop(columns='race_date')
    df_test = df[df.race_date == date].drop(columns='race_date')
    train_cols = [x for x in df_train.columns if x != 'ps']
    
    X_train = df_train[train_cols]
    y_train = df_train['ps']
    X_test = df_test[train_cols]
    y_test = df_test['ps']
    
    model.train(X_train, y_train)
    model.test(X_test, y_test)

    opt = Optimizer(model.predictions)
    opt.solve()
    opt.get_lineup()
    
    performance[date] = {
        "rmse": model.performance,
        "lineup": opt.lineup
    }

print(performance)
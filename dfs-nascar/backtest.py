import pandas as pd
import numpy as np

from nascar_lineups.clean_data import LoadData
from nascar_lineups.optimizer import Optimizer
from nascar_lineups.model import Model
#from sklearn.preprocessing import power_transform

load = LoadData('./tmp.ini', 'nascar_linestar')
load.setup_connection()
load.create_df()
load.data_clean()

# for col in load.df.columns:
#     if (load.df[col].dtype == 'float' or load.df[col].dtype == 'int') and col != 'ps' and col != 'salary':
#         try:
#             load.df[col] = power_transform(load.df[col].values.reshape(-1, 1))
#         except:
#             pass
df = load.df.copy()
#df['practice_best_lap_time'] = df['practice_best_lap_time'] * (df['miles'] / df['laps'])
#df['qualifying_best_lap_time'] * (df['miles'] / df['laps'])
df.drop(columns=[x for x in df.columns if '_name_' in x], inplace=True)

#from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import BayesianRidge
model = BayesianRidge()
params = ['']
model = Model(model, params)

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
    
    results = df_test[df_test['name'].isin(opt.lineup)]

    performance[date] = {
        "score": results['ps'].sum(),
        'salary': results['salary'].sum(),
        #'projected': model.predictions[model.predictions.name.isin(results.name)]
    }
    

import pprint
pprint.pprint(performance)
pprint.pprint(model.col_names)
score = []
for date in performance.keys():
    score.append(performance[date]['score'])
print('Final Score:', pd.Series(score).mean())

salary = []
for date in performance.keys():
    salary.append(performance[date]['salary'])
print('Final Salary:', pd.Series(salary).mean())

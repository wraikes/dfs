import pandas as pd
import numpy as np

from nascar_lineups.clean_data import LoadData
from nascar_lineups.optimizer import Optimizer
from nascar_lineups.model import Model

load = LoadData('./tmp.ini', 'nascar_linestar')
load.setup_connection()
load.create_df()
load.data_clean()
df = load.df.copy()

#from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
params = []
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
    
    performance[date] = {
        "rmse": model.performance,
        "lineup": opt.lineup,
        'data': model.predictions
    }

print(performance)

rmse = []
for date in performance.keys():
    rmse.append(performance[date]['rmse'])
print(pd.Series(rmse).mean())


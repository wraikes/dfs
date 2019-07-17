import pandas as pd
import numpy as np

from load_data import get_data
from build_model import Model, Performance

df = get_data()
model = Model()
performance = Performance()

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
    
    performance.record(model)

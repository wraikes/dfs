import pandas as pd
import numpy as np
import joblib

from preprocessing.pp_mma import *
from optimizer.optimizer_mma import Optimizer
from etl.etl_raw_data import RawDataLine
from etl.etl_process_data import LinestarETL

from config import config
import warnings

def dedupe(data):
    gids = data.groupby('GID').size()
    gids = gids[gids==2].index.to_list()
    
    data = data[data.GID.isin(gids)]

    return data
    

def predict(data, site):
    #load pipelines (should be numerous)
    pipes = joblib.load(f'./models/pipes_mma_{site}.pkl')

    #loop thru pipelines
    for i, pipe in enumerate(pipes):
    	data['preds_{i}'] = pipe.predict(data[config.ALL_COLS])

    #aggregate
    data['preds'] = data[[x for x in data.columns if 'preds' in x]].mean(axis=1)

    return data


def optimize(data, site):
    opt = Optimizer(data, 'mma', site)
    opt.solve()
    opt.get_lineup()

    return opt.lineup


if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    #pull new projection data
    raw_data = RawDataLine('mma')
    raw_data.pull_data()

    #process projection data
    data = LinestarETL('mma', True)
    data.extract()
    data.transform()
    data.load()

    for site in ['fd', 'dk']:
        print(f'{site}:')

        #load projection data
        data_ = data.final_df[site].copy()
        data_ = dedupe(data_)
        
        #make predictions & lineups
        df = predict(data_, site)
        lineup = optimize(df, site)

        #print lineups
        print(df[df.Name.isin(lineup)][['Name', 'preds', 'SAL']].sort_values(by='preds'))




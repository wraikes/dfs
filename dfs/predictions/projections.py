import pickle
import boto3
import pandas as pd
import numpy as np
import json

from model.optimizer import Optimizer

def get_post_preds(i, trace, preds_scale, idx):
    beta_range = trace.beta.shape[1]

    pred = np.random.normal(
        np.array(trace['alpha'][:, idx] + [trace['beta'][:, j]*preds_scale[i, j] for j in range(beta_range)]).sum(axis=0),
        trace['sigma']
    )
    
    return pred
    
    
def get_lineup(df, sport, site):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    if sport == 'nba':
        constants = ['name', 'pos', 'event_id']
        model_variables = ['pp', 'ppg', 'salary', 'lovecount', 'hatecount']
        
        #need to replace this
        #df = df[df.oteam.isin(['LAC', 'DEN', 'PHO', 'CHA'])]
        #df = df[df.oteam.isin(['CHI', 'NO', 'NY', 'UTA', 'MIL', 'GS'])]
        #df = df[df.oteam.isin(['NY', 'UTA', 'MIL', 'GS'])]
        df = df[df.name != 'Anthony Davis']
        
    elif sport == 'pga':
        constants = ['name', 'event_id']
        model_variables = ['pp', 'ppg', 'salary', 'vegas_odds_0', 'vegas_value_0']
        
    for col in model_variables:
        df[col] = pd.to_numeric(df[col])
            
    df_tmp = df[constants+model_variables].dropna()
    preds = df_tmp[df_tmp.event_id==df.event_id.max()]
        
    obj = pickle.loads(s3.Bucket("my-dfs-data").Object("{}/modeling/model_{}.pkl".format(sport, site)).get()['Body'].read())
    trace, scaler, player_ids = obj[0], obj[1], obj[2]
    
    preds = preds.merge(player_ids, how='left', on='name')
    tmp_preds = scaler.transform(preds[model_variables])

    preds['posterior'] = None

    for i, name in enumerate(preds.name):
        idx = preds.loc[preds.name==name, 'player_idx'].values[0]
        if not np.isnan(idx):
            preds.loc[preds.name==name, 'posterior'] = [[get_post_preds(i, trace, tmp_preds, idx)]]
        else:
            print(name)
            preds.loc[preds.name==name, 'posterior'] = np.nan
    
    preds = preds.dropna()
    preds['preds'] = preds['posterior'].apply(lambda x: np.median(x[0]))#.median())

    #use optimizer for lineups
    opt = Optimizer(preds, sport, site)
    opt.solve()
    opt.get_lineup()

    return opt.lineup


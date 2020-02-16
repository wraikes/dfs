import pickle
import boto3
import pandas as pd
import numpy as np
import json

from model.optimizer import OptimizerNascar

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

        
    elif sport == 'pga':
        constants = ['name', 'event_id']
        model_variables = ['pp', 'ppg', 'salary', 'vegas_odds_0', 'vegas_value_0']
    
    elif sport == 'nascar':
        constants = ['name', 'ps', 'event_id']
        model_variables = [    
            'sal',
            'pp',
            'practice_laps_1',
            'races_4',
            'finished_4',
            'wins_4',
            'top_5s_4',
            'avg_place_4',
            'practice_best_lap_time_rank'
        ]
    
    for col in model_variables:
        df[col] = pd.to_numeric(df[col])

    obj = pickle.loads(s3.Bucket("my-dfs-data").Object("{}/modeling/model_{}.pkl".format(sport, site)).get()['Body'].read())
    trace, scaler, player_idx = obj[0], obj[1], obj[2]

    preds = df.loc[df.event_id==df.event_id.max(), constants+model_variables].dropna()
    preds_scale = scaler.transform(preds[model_variables])
    preds['posterior'] = None
    n_betas = len(model_variables)


    
    preds = preds.merge(player_idx, how='left', on='name').drop_duplicates()

    for idx in range(preds.shape[0]):
        player_idx = preds.iloc[idx]['player_idx']
        if np.isnan(player_idx):
            continue
        else:
            player_idx = int(player_idx)
        values = np.array(trace['alpha'][:, player_idx] + [trace['beta'][:, j]*preds_scale[idx, j] for j in range(n_betas)]).mean(axis=0)
        preds.loc[preds['player_idx']==player_idx, 'posterior'] = [[values]]


    preds = preds.dropna()
    preds = preds[preds.races_4 > 60]
    #preds['posterior'] = np.where(preds['posterior'] is None, [[0]], preds['posterior'])
    #preds.dropna(inplace=True)
    preds['preds'] = preds['posterior'].apply(lambda x: np.mean(x[0]))

    #use optimizer for lineups

    opt = OptimizerNascar(preds, site)
    opt.get_lineup()

    return opt.lineup


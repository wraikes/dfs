import pymc3 as pm
import pandas as pd
import numpy as np
import pickle
import boto3
from sklearn.preprocessing import StandardScaler


def build_model(df, sport, site):
    '''
    constants: event_id, name, ps, [pos]
    '''
    event_id = df.event_id.max()
    
    if sport == 'nba':
        constants = ['name', 'pos', 'ps', 'event_id']
        model_variables = ['pp', 'ppg', 'salary', 'lovecount', 'hatecount']
        
    elif sport == 'pga':
        constants = ['name', 'ps', 'event_id']
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
    n_betas = len(model_variables)

    df = df[df.projections=='false']
    tmp = df[constants+model_variables].dropna()

    X = tmp[tmp.event_id < event_id]
    X['player_idx'] = X.name.astype('category').cat.codes
    
    n_players = len(X.player_idx.unique())
    player_idx = [int(x) for x in X.player_idx]
    
    scaler = StandardScaler()
    X_scale = scaler.fit_transform(X[model_variables])
    
    with pm.Model() as model:
        
        # Hyperpriors for group nodes
        mu_a = pm.Normal('mu_a', mu=45, sigma=20)
        sigma_a = pm.HalfNormal('sigma_a', 15)
    
        # Priors
        alpha = pm.Normal('alpha', mu=mu_a, sigma=sigma_a, shape=n_players)
        beta = pm.Normal('beta', mu=2, sigma=15, shape=n_betas)
        sigma = pm.HalfNormal('sigma', 15)
    
        # Link function
        mu = alpha[player_idx] + [beta[x]*X_scale[:, x] for x in range(n_betas)]
    
        # Data likelihood
        Y_obj = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=X['ps'])
    
        trace = pm.sample(300, chains=2)

    player_idx = X[['name', 'player_idx']]
    obj = pickle.dumps([trace, scaler, player_idx])
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    s3.Object(bucket.name, '{}/modeling/model_{}.pkl'.format(sport, site)).put(Body=obj)

    

if __name__ == '__main__':
    pass

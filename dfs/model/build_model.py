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
        n_beta = len(model_variables)
    
    df = df[df.projections=='false']
    df_tmp = df[constants+model_variables].dropna()
    
    X_train = df_tmp[df_tmp.event_id < event_id]
    X_train['player_idx'] = None
    for name, val in zip(X_train.name.unique(), range(len(X_train.name.unique()))):
        X_train['player_idx'] = np.where(X_train.name==name, val, X_train['player_idx'])

    player_idx = pd.to_numeric(X_train.player_idx).values
    n_player = len(X_train.player_idx.unique())

    scaler = StandardScaler()
    X_scale = scaler.fit_transform(X_train[model_variables])
    player_ids = X_train[['name', 'player_idx']].drop_duplicates()
    
    with pm.Model() as model:
        # Hyperpriors for group nodes
        mu_a = pm.Normal('mu_a', mu=0., sigma=100)
        sigma_a = pm.HalfNormal('sigma_a', 5)

        alpha = pm.Normal('alpha', mu=mu_a, sigma=sigma_a, shape=n_player)
        beta = pm.Normal('beta', mu=0, sigma=10, shape=n_beta)
        sigma = pm.HalfCauchy('sigma', 5)

        mu = alpha[player_idx] + [beta[x]*X_scale[:, x] for x in range(n_beta)]

        # Data likelihood
        Y_obj = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=X_train['ps'])

        trace = pm.sample(150, chains=1)  

    obj = pickle.dumps([trace, scaler, player_ids])
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    s3.Object(bucket.name, '{}/modeling/model_{}.pkl'.format(sport, site)).put(Body=obj)

    

if __name__ == '__main__':
    pass

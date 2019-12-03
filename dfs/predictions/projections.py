import pickle
import boto3
import pandas as pd
import numpy as np
import json

from predictions.optimizer import Optimizer

from pga.prep_data import prep_data

def get_lineup(df, sport, site):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    df = prep_data(df)
    df = df[df.projections=='true']
    df = df.fillna(0) #this should not be needed, should be in prep_data

    obj = pickle.loads(s3.Bucket("my-dfs-data").Object("{}/modeling/model_{}.pkl".format(sport, site)).get()['Body'].read())
    
    for col in obj[1]:
        if col not in df.columns:
            df[col] = 0
        else:
            df[col] = pd.to_numeric(df[col])
    
    df['preds'] = obj[0].predict(df[obj[1]])

    #use optimizer for lineups
    opt = Optimizer(df, sport, site)
    opt.solve()
    opt.get_lineup()

    return opt.lineup



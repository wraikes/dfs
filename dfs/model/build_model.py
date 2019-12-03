# pull data from rds, load into pandas
# train model with selected parameters (or load via prototype?)
# save model

import boto3
import pandas as pd
import numpy as np
import pickle

from pga.prep_data import prep_data

class Model:
    def __init__(self, model, params, df):
        self.model = model
        self.params = params
        self.df = df
    
    def _prep_data(self):
        self.df = prep_data(self.df)
        self.df = self.df[self.df.projections=='false']
        self.df.drop(columns='projections', inplace=True)
        self.df = self.df.fillna(0) #this should not be needed, should be in prep_data
        
    def train(self):
        self._prep_data()

        X = self.df.drop(columns=['name', 'ps'])
        y = self.df['ps']

        self.col_names = X.columns
        self.model.fit(X, y)
    
    def save(self, sport, site):
        obj = pickle.dumps([self.model, self.col_names])
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-dfs-data')
        s3.Object(bucket.name, '{}/modeling/model_{}.pkl'.format(sport, site)).put(Body=obj)

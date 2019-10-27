# pull data from rds, load into pandas
# train model with selected parameters (or load via prototype?)
# save model

import boto3
import pandas as pd
import numpy as np
import pickle


class Model:
    def __init__(self, model, params):
        self.model = model
        self.params = params


    def train(self, X, y):
        X = X.drop(columns='name')
        self.col_names = X.columns
        self.model.fit(X.values, np.ravel(y))
    
    
    def save(self):
        obj = pickle.dumps([self.model, self.col_names])
        
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-dfs-data')
        s3.Object(bucket.name, 'modeling/nascar.pkl').put(Body=obj)


import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error

class Model:
    def __init__(self, model, params):
        self.model = model
        self.params = params
        
        self.col_names = []
        self.predictions = None
        self.performance = None


    def train(self, X_train, y_train):
        X_train = X_train.drop(columns='name')
        self.col_names = X_train.columns
        self.model.fit(X_train.values, np.ravel(y_train))
    

    def test(self, X_test, y_test):
        X_test['preds'] = self.model.predict(X_test.drop(columns='name'))
        
        self.performance = mean_squared_error(y_test, X_test['preds'])**0.5
        self.predictions = X_test[['name', 'salary', 'preds']]
    
    
    def save(self, path):
        obj = [self.model, self.col_names]
        pickle.dump(obj, path)
        
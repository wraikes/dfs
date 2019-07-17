import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

class Model:
    
    def __init__(self, model, params):
        self.model = model
        self.params = params
        self.predictions = None
        self.performance = None
        
        self.model = None
        

    def train(self, X_train, y_train):
        self.model.fit(X_train.drop(columns='name'), y_train)
    

    def test(self, X_test, y_test):
        X_test['preds'] = self.model.predict(X_test.drop(columns='name'))
        self.performance = mean_squared_error(y_test, X_test['preds'])**0.5
        self.predictions = X_test[['name', 'salary', 'preds']]

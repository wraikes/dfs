import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class GidString(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X['GID'] = X['GID'].astype('str')

        return X        


class NumImputer(BaseEstimator, TransformerMixin):
    #for reoccuring players (not mma), groupby name for means
    #X.groupby('name')[var].apply(lambda x: x.fillna(x.median()))

    def __init__(self, vars):
        self.vars = vars + ['impute']
        
        self.cache = {}
        self.sal_means = None

    def fit(self, X, y=None):
        self.sal_means = X.groupby('SAL').mean().reset_index()

        return self

    def transform(self, X, y=None):
        X = X.merge(self.sal_means, how='left', on='SAL', suffixes=['', '_impute'])
        X['impute'] = np.where(X['PP']==51.1, 1, 0)
        
        for var in self.vars:
            if var in ['SAL', 'impute', 'GID', 'Name']:
                continue
            elif var == 'PP':
                X[var] = np.where(X[var]==51.1, X[f'{var}_impute'], X[var])
            else:
                X[var] = np.where((X[var]==0) | (X[var].isnull()), X[f'{var}_impute'], X[var]) 
        
        X = X.drop(columns=[x for x in X.columns if x.endswith('_impute')])
        
        for var in self.vars:
            if var in ['SAL', 'impute', 'GID', 'Name']:
                continue
            else:
                X[var] = np.where(X[var].isnull(), X[var].median(), X[var])
        
        return X[self.vars]
    

class OppCols(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.vars = None
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        self.vars = list(X.columns)
        self.vars += [f'{x}_opp' for x in self.vars if x not in ['GID', 'Name']]

        X = X.merge(X, on='GID', how='left', suffixes=['', '_opp'])
        X = X[X.Name != X.Name_opp]
        
        X = X[self.vars]
        X.drop(columns=['Name', 'GID'], inplace=True)
        
        return X


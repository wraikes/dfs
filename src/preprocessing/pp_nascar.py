import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


# class CareerAvg(BaseEstimator, TransformerMixin):
# 	def __init__(self, var):
# 		self.var = var

# 	def fit(X, y=None):
# 		return self

# 	def transform(X, y=None):
# 		X['rank'] = X.groupby('date')['ps'].rank(ascending=False)
# 		X['career_average'] = X.groupby('name')['rank'].transform('mean')
#     	X['career_std'] = X.groupby('name')['rank'].transform('std')
#     	X['career_std'] = X['career_std'].fillna(df['career_std'].median())

#### MOVE BACK TO BASE
class MissingNum(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		for var in self.vars:
			X[f'{var}_NA'] = np.where(X[var].isnull(), 1, 0)
			X[var] = X.groupby('name')[var].apply(lambda x: x.fillna(x.median()))

		return X
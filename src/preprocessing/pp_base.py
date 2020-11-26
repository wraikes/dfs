import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


class CatImputer(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		for var in self.vars:
			X.loc[:, var] = X.loc[:, var].fillna('NA')

		return X


class DateColumns(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		for var in self.vars:
			X.loc[:, f'{var}_DAY'] = X.loc[:, var].dt.day
			X.loc[:, f'{var}_MONTH'] = X.loc[:, var].dt.month
			X.loc[:, f'{var}_YEAR'] = X.loc[:, var].dt.year

		return X


class NumImputer(BaseEstimator, TransformerMixin):
	#for reoccuring players (not mma), groupby name for means
	#X.groupby('name')[var].apply(lambda x: x.fillna(x.median()))

	def __init__(self, vars):
		self.vars = vars
		self.cache = {}

	def fit(self, X, y=None):
		for var in self.vars:
			self.cache[var] = X[var].median()

		return self

	def transform(self, X, y=None):
		for var in self.vars:
			X.loc[:, f'{var}_NA'] = np.where(X[var].isnull(), 1, 0)
			X.loc[:, var] = X[var].fillna(self.cache[var])

		return X


# class OneHotEncoder(BaseEstimator, TransformerMixin):
# 	def __init__(self, vars):
# 		self.vars = vars

# 	def fit(self, X, y=None):
# 		return self

# 	def transform(self, X, y=None):
# 		for var in self.vars:
# 			X = pd.get_dummies(X, columns=[var])

# 		return X


class DropColumns(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		X = X.drop(columns=self.vars)

		return X



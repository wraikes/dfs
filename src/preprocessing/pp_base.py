import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


class MissingCat(BaseEstimator, TransformerMixin):
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


class MissingNum(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		for var in self.vars:
			X.loc[:, f'{var}_NA'] = np.where(X[var].isnull(), 1, 0)
			X.loc[:, var] = X.groupby('name')[var].apply(lambda x: x.fillna(x.median()))
			X.loc[:, var] = X[var].fillna(X[var].median())

		return X


class OneHotEncoder(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		for var in self.vars:
			X = pd.get_dummies(X, columns=[var])

		return X


class DropColumns(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(self, X, y=None):
		return self

	def transform(self, X, y=None):
		X = X.drop(columns=self.vars)

		return X



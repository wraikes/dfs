import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


class MissingCat(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		for var in self.vars:
			X[var].fillna('NA', inplace=True)

		return X


class DateColumns(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		for var in self.vars:
			X[f'{var}_DAY'] = X[var].dt.day
			X[f'{var}_MONTH'] = X[var].dt.month
			X[f'{var}_YEAR'] = X[var].dt.year


class OneHotEncoder(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		for var in self.vars:
			X = pd.get_dummies(X, columns=[var])

		return X





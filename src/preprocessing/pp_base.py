import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

class MissingNum(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		for var in self.vars:
			X[var] = X.groupby('name')[var].apply(lambda x: x.fillna(x.median()))

		return X


class MissingCat(BaseEstimator, TransformerMixin):
	def __init__(self, vars):
		self.vars = vars

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		for var in self.vars:
			X[var].fillna('NA', inplace=True)

		return X











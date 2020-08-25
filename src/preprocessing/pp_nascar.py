import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


class CareerAvg(BaseEstimator, TransformerMixin):
	def __init__(self, var):
		self.var = var

	def fit(X, y=None):
		return self

	def transform(X, y=None):
		X['career_average'] = X.groupby('name')['rank'].transform('mean')
    	X['career_std'] = X.groupby('name')['rank'].transform('std')
    	X['career_std'] = X['career_std'].fillna(df['career_std'].median())


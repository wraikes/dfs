import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin


class CareerAvg(BaseEstimator, TransformerMixin):
    df['career_average'] = df.groupby('name')['rank'].transform('mean')
    df['career_std'] = df.groupby('name')['rank'].transform('std')
    df['career_std'] = df['career_std'].fillna(df['career_std'].median())


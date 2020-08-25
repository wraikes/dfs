import pandas as pd
import numpy as np
import joblib
import sys

from pipelines import pipe_nascar as pipe
from config import config

def train_pipeline():
	sport = sys.argv[1]

	#load data
	df = pd.read_csv('../data/nascar_fd.csv', parse_dates=['date'])

	#fit pipeline
	pipe.fit(X=df[config.ALL_COLS], y=df[config.TARGET])

	#save trained model
	joblib.dump(pipe, f'./train_models/mdl_{sport}.pkl')



if __name__ == '__main__':
	train_pipeline()





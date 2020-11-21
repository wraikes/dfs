import pandas as pd
import numpy as np
import joblib

from config import config

# pull new projection data
# transform projection data
# predict data (done)
# optimize prediction and print lineups

def predict(data):
	#load pipeline
	pipe = joblib.load('./trained_models/mdl_nascar.pkl')

	#predict
	predictions = pipe.predict(data[config.ALL_COLS])

	return predictions


if __name__ == '__main__':

	#pull projection data
	####TODO

	#transform projection data
	df = pd.read_csv('../data/nascar_fd.csv', parse_dates=['date'])
	df = df[df.projections==True]

	preds = predict(df)

	for name, pred in zip(df.name, preds):
		print(f'{name}: {pred}')


import pandas as pd
import numpy as np
import joblib

from optimizer.optimizer_mma import Optimizer
from etl.etl_raw_data import RawDataLine
from etl.etl_process_data import LinestarETL

from config import config

# pull new projection data
# transform projection data
# predict data (done)
# optimize prediction and print lineups

def predict(data):
	#load pipeline
	pipe = joblib.load('./trained_models/mdl_mma.pkl')

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




# if __name__ == '__main__':
# 	model = joblib.load('./models/mma_model.pkl')
	
# 	df_fd = pd.read_csv('./')
# 	df_dk = pd.read_csv('./')

# 	pull = RawDataLine('mma')
# 	pull.pull_data()

# 	process = LinestarETL('mma', True)
# 	process.extract()
# 	process.transform()
# 	process.load()

# 	df = process.final_df.copy()


# 	cols = [
# 	    'SAL', 'PP', 'Max Rounds_0',
# 	    'Vegas Odds_0', 'Full Fight Odds_0', 'SS Landed/F_1', 'SS Landed/Min_1',
# 	    'Strike Acc%_1', 'Takedowns/F_1', 'Rounds/F_1', 'Win%_1', 'FPPG_1',
# 	    'SS Taken/F_2', 'SS Taken/Min_2', 'Strike Def%_2',
# 	    'Takedowns Taken/F_2', 'Takedown Def%_2', 'FPPG Allowed_2',
# 	    'SS Landed/F_3', 'SS Landed/Min_3', 'Strike Acc%_3', 'Takedowns/F_3',
# 	    'Rounds/F_3', 'Win%_3', 'FPPG_3', 'SS Taken/F_4', 'SS Taken/Min_4',
# 	    'Strike Def%_4', 'Takedowns Taken/F_4', 'Takedown Def%_4',
# 	    'FPPG Allowed_4', 'Win Pct_0'
# 	]


# 	df['preds'] = model.predict(df[cols].fillna(0))













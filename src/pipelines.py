from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor

from preprocessing import pp_base
from preprocessing import pp_mma
from config import config

pipe_mma = make_pipeline(
	pp_base.MissingCat(config.CAT_COLS),
	GradientBoostingRegressor(
		learning_rate=0.01, 
		max_depth=4, 
		n_estimators=300, 
		max_features='sqrt', 
		random_state=4
	)
)


if __name__ == '__main__':
	import pandas as pd
	df = pd.read_csv('../data/nascar_fd.csv', parse_dates=['date'])

	pipe_nascar.fit(df[config.ALL_COLS], df[config.TARGET])



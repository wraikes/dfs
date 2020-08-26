from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingRegressor

from preprocessing import pp_base
from preprocessing import pp_nascar
from config import config

pipe_nascar = make_pipeline(
	pp_base.MissingCat(config.CAT_COLS),
	pp_base.DateColumns(config.DATE_COLS),
	pp_base.OneHotEncoder(config.CAT_COLS),
	pp_base.MissingNum(config.NUM_COLS),
	pp_base.DropColumns(config.DROP_COLS),
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



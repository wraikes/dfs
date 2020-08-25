from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor

from preprocessing import pp_base
from preprocessing import pp_nascar
from config import config

pipe_nascar = make_pipeline([
	pp_base.MissingCat(config.CAT_COLS),
	pp_base.DateColumns(config.DATE_COLS),
	pp_nascar.MissingNum(config.NUM_COLS),
	RandomForestRegressor()
])





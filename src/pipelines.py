from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor

from preprocessing import pp_base
from preprocessing import pp_nascar as pp
from preprocessing import pp_mma as pp


pipe_nascar = make_pipeline([
	pp_base(),
	pp_nascar(),
	RandomForestRegressor()
])



pipe_mma = make_pipeline([
	pp_base(),
	pp_mma(),
	RandomForestRegressor()
])


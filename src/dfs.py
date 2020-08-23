#python3 dfs [--sport] [--pull raw data]
#- pull raw data: updates non projection data & model

import sys

from data_mgmt.etl_raw_data import RawDataLine
from data_mgmt.etl_process_data import ProcessDataLine

#from etl.etl_pipeline import etl
#from etl.combine_data import create_dataframe
#from model.build_model import build_model
#from predictions.projections import get_lineup


def dfs(sport):
    
    #pull new data
    line_raw = RawDataLine(sport)
    line_raw.update_data()

    #etl data from s3 into rds
    line_process = ProcessDataLine(sport)
    line_process.extract()
    line_process.transform()
    ##line_process.load()

    #process new data from rds
    ##feature engineering/processing

    #make predictions
    ##load model
    ##make predictions
    ##optimize


if __name__ == '__main__':
    import pdb; pdb.set_trace()
    dfs(sys.argv[1])

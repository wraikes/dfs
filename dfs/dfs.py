#python3 dfs [--sport] [--pull raw data]
#- pull raw data: updates non projection data & model

import sys

from etl_raw_data import linestarapp
#from etl.etl_pipeline import etl
#from etl.combine_data import create_dataframe
#from model.build_model import build_model
#from predictions.projections import get_lineup


def dfs(sport, update_data, update_model):
    
    #pull new data into s3
    if update_data=='True':
        #linestarapp
        pull_linestar_data = linestarapp.PullData(sport)
        pull_linestar_data.update_data()
        
        #sportsline
        

    #process s3 data into rds
    

    #update model
    if update_model=='True':
        pass
    

    #make predictions



if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2], sys.argv[3])

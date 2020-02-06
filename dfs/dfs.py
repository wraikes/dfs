#python3 dfs [--sport] [--pull raw data]
#- pull raw data: updates non projection data & model

import sys

from scrapers.scrapers import LinestarappData, SportslineData, FantasyNerdData

from etl.etl import *

from etl.combine_data import create_dataframe
from model.build_model import build_model
from predictions.projections import get_lineup


def dfs(sport, update, new_model):
    sites = ['fd', 'dk']
    for site in sites: #need to work out dk

        if update=='True':
            linestarapp = LinestarappData(sport, site)
            linestarapp.update_data()
            
        etl_linestarapp = LinestarappETL(sport)   
        etl_linestarapp.extract()
        etl_linestarapp.transform()
        etl_linestarapp.load()

        # ### combine all data to a saved rds table
        # df = create_dataframe(sport, site, save=True)
        
        # if new_model=='True':
        #     #update model & save to s3
        #     build_model(df, sport, site)

        # #if projections exist, then get lineups
        # lineup = get_lineup(df, sport, site)
        # print('{}: {}'.format(site, lineup))



if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2], sys.argv[3])

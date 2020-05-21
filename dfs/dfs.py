#python3 dfs [--sport] [--pull raw data] [--update model]
#- pull raw data: updates non projection data & model

import sys

from scrapers.scrapers import LinestarappData, SportslineData, FantasyNerdData

from etl.etl import *

from etl.combine_data import pull_tables, clean_data
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
            
    for site in sites:
        
        df = pull_tables(sport, site)
        df = clean_data(df, sport)

        if new_model=='True':
            build_model(df, sport, site)

        lineup = get_lineup(df, sport, site)
        print('{}: {}'.format(site, lineup))


if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2], sys.argv[3])

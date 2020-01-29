#python3 dfs [--sport] [--pull raw data]
#- pull raw data: updates non projection data & model

import sys

from raw_data_pull.etl import LinestarappData, SportslineData, NerdfantasyData
from etl.etl_pipeline import etl
from etl.combine_data import create_dataframe
from model.build_model import build_model
from predictions.projections import get_lineup


def dfs(sport, update, new_model):
    sites = ['fd'] if sport == 'nba' else ['fd', 'dk']
    for site in sites: #need to work out dk
        #update data
        if update=='True':
            
            linestarapp = LinestarappData(sport, site)
            linestar.update_data()
            
            #todo: sportsline, nerdfantasy
            
        ### etl: s3 to rds
        etl(sport, 'linestarapp')
        #etl(sport, 'sportsline')
        #if sport in ['nfl', 'nba', 'nhl', 'mlb']
        #    etl(sport, 'nerd')
    
        ### combine all data to a saved rds table
        df = create_dataframe(sport, site, save=True)
        
        if new_model=='True':
            #update model & save to s3
            build_model(df, sport, site)

        #if projections exist, then get lineups
        lineup = get_lineup(df, sport, site)
        print('{}: {}'.format(site, lineup))



if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2], sys.argv[3])

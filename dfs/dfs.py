#python3 dfs [--sport] [--pull raw data] [--get projections]
#- pull raw data: updates non projection data & model
#- get projections: updates projection data and get projections

import sys

from raw_data_pull.raw_data_pull import pull_data

from etl.etl_pipeline import etl
from etl.combine_data import create_dataframe
from model.update_model import update_model
from predictions.projections import get_lineup


def dfs(sport, update):

    for site in ['fd', 'dk']:
        #update data
        if update=='True':
            pull_data(sport, site)

        ### etl: s3 to rds
        etl(sport, 'linestarapp')
        #etl(sport, 'sportsline')
        #if sport in ['nfl', 'nba', 'nhl', 'mlb']
        #    etl(sport, 'nerd')
    
        ### combine all data to a saved rds table
        df = create_dataframe(sport, site, save=True)
        
        #update model & save to s3
        update_model(df, sport, site)

        #if projections exist, then get lineups
        lineup = get_lineup(df, sport, site)
        print('{}: {}'.format(site, lineup))



if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2])
    
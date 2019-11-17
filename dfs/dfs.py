#python3 dfs [--sport] [--pull raw data] [--get projections]
#- pull raw data: updates non projection data & model
#- get projections: updates projection data and get projections

import sys

from helpers.database_connection import connect_to_database
from raw_data_pull.raw_data_pull import pull_data

from nascar.etl_pipeline import etl
from nascar.etl.combine_data import create_table
from nascar.update_model import update_model
from nascar.projections import get_lineup

#from pga.etl_pipeline import etl
#from pga.etl.combine_data import create_table
#from pga.update_model import update_model
#from pga.projections import get_lineup

def dfs(sport):
    cur = connect_to_database()
    
    #update data
    #pull_data(sport, 'fd')
    #pull_data(sport, 'dk')

    ### etl: s3 to rds
    etl('sportsline', cur)
    etl('linestarapp', cur)
    
    ### combine all data to a saved rds table
    df_fd = create_table(cur, 'fd', save=True)
    df_dk = create_table(cur, 'dk', save=True)
        
    #update model & save to s3
    update_model(df_fd, 'fd')
    update_model(df_dk, 'dk')
    
    #if projections exist, then get lineups
    lineup_fd = get_lineup(cur, 'fd')
    lineup_dk = get_lineup(cur, 'dk')
    print('FanDuel {}'.format(lineup_fd))
    print('DraftKings: {}'.format(lineup_dk))


if __name__ == '__main__':
    dfs('nascar')
    
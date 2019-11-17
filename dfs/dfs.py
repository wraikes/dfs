#python3 dfs [--sport] [--pull raw data] [--get projections]
#- pull raw data: updates non projection data & model
#- get projections: updates projection data and get projections

import sys

from database_connection.database_connection import connect_to_database
from raw_data_pull.raw_data_pull import pull_data

from nascar.etl_pipeline import etl
from nascar.etl.combine_data import create_table
from nascar.update_model import update_model
from nascar.projections import get_lineup

from pga.etl_pipeline import etl
from pga.etl.combine_data import create_table
from pga.update_model import update_model
from pga.projections import get_lineup

def dfs(sport, update):
    cur = connect_to_database()
    
    for site in ['fd', 'dk']:
        #update data
        if update==True:
            pull_data(sport, site)

        ### etl: s3 to rds
        etl(cur, sport)
    
        ### combine all data to a saved rds table
        df = create_table(cur, site, save=True)
        
        #update model & save to s3
        update_model(df, site)

        #if projections exist, then get lineups
        lineup = get_lineup(cur, site)
        print('{}: {}'.format(site, lineup))



if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2])
    
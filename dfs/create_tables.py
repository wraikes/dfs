#create nascar tables; script only runs once
import sys

from create_tables.sql_queries import *
from database_connection.database_connection import connect_to_database

def create_table(sport, drop=False):
    cur = connect_to_database()

    if drop:
        cur.execute(drop_linestarapp_table.format(sport, 'dk'))
        cur.execute(drop_linestarapp_table.format(sport, 'fd'))
    
        for table in ['leaderboard', 'dfs_pro', 'betting']:
            cur.execute(drop_sportsline_table.format(sport, table))

    for site in ['dk', 'fd']:
        if sport == 'nascar':
            cur.execute(nascar_linestarapp_create_table.format(site))

        elif sport == 'pga':
            cur.execute(pga_linestarapp_create_table.format(site))        
    
    cur.execute(sportsline_pro_create_table.format(sport))
    cur.execute(sportsline_leaderboard_create_table.format(sport))
    cur.execute(sportsline_betting_create_table.format(sport))


if __name__=='__main__':
    create_table(sys.argv[1], sys.argv[2])

#create nascar tables; script only runs once
import sys

from sql_queries import *
from database_connection import connect_to_database

cur = connect_to_database()

cur.execute('DROP TABLE IF EXISTS nascar_linestarapp')
cur.execute('DROP TABLE IF EXISTS nascar_sportsline_leaderboard')
cur.execute('DROP TABLE IF EXISTS nascar_sportsline_betting')
cur.execute('DROP TABLE IF EXISTS nascar_sportsline_dfs_pro')
    
cur.execute(nascar_linestarapp_create_table)
cur.execute(nascar_sportsline_dfs_pro_create_table)
cur.execute(nascar_sportsline_betting_create_table)
cur.execute(nascar_sportsline_leaderboard_create_table)


#create nascar tables; script only runs once
import sys

#from helpers.sql_queries import *
from helpers.database_connection import connect_to_database  ##have to figure out this import

cur = connect_to_database()

# cur.execute('DROP TABLE IF EXISTS nascar_linestarapp_fd')
# cur.execute('DROP TABLE IF EXISTS nascar_linestarapp_dk')
# cur.execute('DROP TABLE IF EXISTS nascar_sportsline_leaderboard')
# cur.execute('DROP TABLE IF EXISTS nascar_sportsline_betting')
# cur.execute('DROP TABLE IF EXISTS nascar_sportsline_dfs_pro')
            
# cur.execute(nascar_linestarapp_fd_create_table)
# cur.execute(nascar_linestarapp_dk_create_table)
# cur.execute(nascar_sportsline_dfs_pro_create_table)
# cur.execute(nascar_sportsline_betting_create_table)
# cur.execute(nascar_sportsline_leaderboard_create_table)

cur.execute('DROP TABLE IF EXISTS pga_linestarapp_fd')
cur.execute('DROP TABLE IF EXISTS pga_linestarapp_dk')
cur.execute('DROP TABLE IF EXISTS pga_sportsline_dfs_pro')
cur.execute('DROP TABLE IF EXISTS pga_sportsline_picks')

cur.execute(pga_linestarapp_fd_create_table)
cur.execute(pga_linestarapp_dk_create_table)
cur.execute(pga_sportsline_dfs_pro_create_table)
cur.execute(pga_sportsline_picks_create_table)

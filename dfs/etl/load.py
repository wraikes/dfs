import psycopg2

from etl.sql_queries import *
from etl.variables import get_variables
from database_connection.database_connection import connect_to_database

# def _insert_sportsline_dfs_pro(cursor, data, sport):
#     cursor.execute(sportsline_pro_insert.format(sport), (
#         data['link_pro'],
#         data['title_pro'],
#         data['date_pro'],
#         data['name'],
#         data['dfs_pick_dk'] if 'dfs_pick_dk' in data.keys() else None
#     )
# )


# def _insert_sportsline_picks(cursor, data, sport):
#     cursor.execute(sportsline_picks_insert.format(sport), (
#         data['link_picks'],
#         data['title_picks'],
#         data['date_picks'],
#         data['name'],
#         data['pos_picks'] if 'pos_picks' in data.keys() else None
#     )
# )


def insert_linestarapp(data, sport):
    var_keys = get_variables(sport)[0]
    var_col_names = get_variables(sport)[1]
    places = ('%s, ' * (len(var_keys)+1))[:-2]

    with connect_to_database() as cur:
        for site in data.keys():
            cur.execute(query_delete_projections.format(sport, site))
            
            for event in data[site]:
                event_id = list(event.keys())[0]
                for player_id in event[event_id].keys():
                    values = (event_id, ) + tuple([
                        event[event_id][player_id][x] if x in event[event_id][player_id].keys() else None for x in var_keys
                    ])
                    values = tuple(None if val == '-' else val for val in values)
                    
                    cur.execute(
                        query_insert_linestarapp.format(sport, site, var_col_names, places),
                        values
                    )

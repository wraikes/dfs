import psycopg2

from pga.etl.sql_queries import *
from pga.etl.variables import get_raw_vars

def _insert_sportsline_dfs_pro(cursor, data, sport):
    cursor.execute(sportsline_pro_insert.format(sport), (
        data['link_pro'],
        data['title_pro'],
        data['date_pro'],
        data['name'],
        data['dfs_pick_dk'] if 'dfs_pick_dk' in data.keys() else None
    )
)


def _insert_sportsline_picks(cursor, data, sport):
    cursor.execute(sportsline_picks_insert.format(sport), (
        data['link_picks'],
        data['title_picks'],
        data['date_picks'],
        data['name'],
        data['pos_picks'] if 'pos_picks' in data.keys() else None
    )
)


def insert_linestarapp(cursor, data, event_id, sport, site, projections):
    variables = get_raw_vars(sport)
    places = ('%s, ' * (1+len(variables)))[:-2]
    print(len(variables))
    cursor.execute(query_insert_linestarapp.format(sport, site, variables, places),
        (event_id, ) + tuple([data[x] for x in variables]) + (projections, )
)



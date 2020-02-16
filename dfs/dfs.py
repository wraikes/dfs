#python3 dfs [--sport] [--pull raw data]
#- pull raw data: updates non projection data & model

import sys

from scrapers.scrapers import LinestarappData, SportslineData, FantasyNerdData

from etl.etl import *

from etl.combine_data import pull_tables
from model.build_model import build_model
from predictions.projections import get_lineup


def dfs(sport, update, new_model):

    etl_linestarapp = LinestarappETL(sport)   
    etl_linestarapp.extract()
    etl_linestarapp.transform()
    etl_linestarapp.load()

    sites = ['fd', 'dk']
    for site in sites: #need to work out dk

        if update=='True':
            linestarapp = LinestarappData(sport, site)
            linestarapp.update_data()
            
        df = pull_tables(sport, site)
        ####nascar specific, need to refactor
        cols = ['practice_best_lap_time_1', 'practice_best_lap_speed_1', 'finished_4', 'wins_4', 'top_5s_4', 'top_10s_4', 'races_4']
        for col in cols:
            df[col] = pd.to_numeric(df[col])
        df['practice_best_lap_time_rank'] = df.groupby('event_id')['practice_best_lap_time_1'].rank()
        df['practice_best_lap_speed_rank'] = df.groupby('event_id')['practice_best_lap_speed_1'].rank()
        percent_cols = ['finished_4', 'wins_4', 'top_5s_4', 'top_10s_4']

        for col in percent_cols:
            df[col] = df[col] / df['races_4']        
        ####
        
        if new_model=='True':
            build_model(df, sport, site)

        lineup = get_lineup(df, sport, site)
        print('{}: {}'.format(site, lineup))


if __name__ == '__main__':
    dfs(sys.argv[1], sys.argv[2], sys.argv[3])

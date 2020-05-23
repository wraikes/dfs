#todo: Nascar specific, need to scale to other sports 
    #mark 'projections' for relevant s3 objects in diff sport
    #find relevant phrasing for sportsline articles in diff sport 

import json
import requests
import boto3
import configparser


class FantasyNerd:
    pass


# if __name__ == '__main__':
#     sports = {
#         'nascar': 263,
#         'nfl': 133,
#         'mlb': 1310,
#         'nba': 1033,
#         'nhl': 1121,
#         'pga': 222
#     }
    
#     for key, value in sports.items():
#         print(key)
#         data = LinestarappData(key, site='fd')
#         data.pull_historical_data(value)

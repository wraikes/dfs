import pandas as pd
import numpy as np
import boto3
import re
import json
import psycopg2
from datetime import datetime

from database_connection.database_connection import connect_to_database


class ProcessData(sport):

    def __init__(self):
        self.sport = sport
        self.cache_pids = []

    def get_cache_pids(self):
        #load cache
        self.cache_pids = cache[sport]

    def pull_s3_keys(self):
        pass

    def extract(self):
        pass

    def transform(self):
        pass

    def connect_to_database(self):
        pass

    def load(self):
        #store pids in cache
        pass


# def extract(sport):
#     s3 = boto3.resource('s3')
#     bucket = s3.Bucket('my-dfs-data') 
#     data_files = {}
# 
#     for site in ['fd', 'dk']:
#         data_files[site] = []
#         
#         #pid's used to append new data
#         with connect_to_database() as cur:
#             cur.execute('SELECT event_id FROM {}_linestarapp_{}'.format(sport, site))
#             pids = set(x[0] for x in cur.fetchall())
# 
#         #loop thru bucket and extract data
#         for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format(sport, 'linestarapp', site)):
#         
#             #skip objects if folder or projection data
#             if obj.key[-1] == '/':
#                 continue
#             
#             #check if object is projection
#             projections = True if 'projections' in obj.key else False
#             
#             #if file pid not in rds pid keys or file is projections, pull file, else continue        
#             pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
#             if pid in pids and not projections:
#                 continue
#             else:
#                 file = s3.Object('my-dfs-data', obj.key)
#                 data = file.get()['Body'].read()
#                 data = json.loads(data)     
#                 data['projections'] = projections
#                 data_files[site].append(data)
#                 
#     return data_files 

import boto3
import re
import json
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime

from database_connection.database_connection import connect_to_database


class ProcessData(sport):

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    def __init__(self):
        self.sport = sport
        self.cache_pids = []
        self.raw_data = {
            'fd': [],
            'dk': []
        }

    def get_cache_pids(self):
        #load cache
        self.cache_pids = cache[sport]

    def pull_s3_keys(self):
        #pull keys from data sources
        for obj in self.bucket.objects.all():
            if self.sport in obj.key:
                if any([x in obj.key for x in ['linestarapp', 'json']]):
                    pid = int(key.split('/')[-1].split('.')[0].split('_')[1])

                    if pid not in self.cache_pids:
                        self.extract(obj.key)

                if any([x in obj.key for x in ['sportsline', 'FILEEXTENSION']]):
                    pass

    def extract(self, key):
        #extract the data and load in cache
        projections = True if 'projections' in key else False

        if pid not in self.cache_pids:
            file = s3.Object('my-dfs-data', key)
            data = file.get()['Body'].read()
            data = json.loads(data)     
            data['projections'] = projections
            self.raw_data[site].append(data)

    def transform(self):
        #transform cache data
        pass

    def connect_to_database(self):
        pass

    def load(self):
        #store pids in cache
        pass



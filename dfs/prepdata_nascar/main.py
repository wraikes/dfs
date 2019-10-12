import boto3
import pandas as pd
import json
import configparser
import psycopg2

from etl import transform
from etl import load


def main():
    ### connect to database
    try: 
        cur = _connect_to_database()
    else:
        return 'Failed to Connect'

    #pid's used to append new data
    cur.execute('SELECT race_id FROM nascar_linestarapp')
    pids = set(x[0] for x in cur.fetchall())
    
    #initialize bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    # loop thru bucket and extract data
    for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format('nascar', 'linestarapp', 'fd')):
        #skip objects if folder or projection data
        if obj.key[-1] == '/' or 'projections' in obj.key:
            continue
    
        #if file pid not in rds pid keys, pull file, else continue        
        pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
        if pid in pids:
            continue
        else:    
            file = s3.Object('my-dfs-data', obj.key)
            data = file.get()['Body'].read()
            data = json.loads(data)
    
        #transform file into usable dictionary
        data_cache = transform(data)
        
        #load dict into rds as new record
        for player_id in data_cache[pid]:
            load(cur, data_cache[pid][player_id], pid, source='linestarapp')
        

if __name__ == '__main__':
    main()


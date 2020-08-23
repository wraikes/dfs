import boto3
import re
import json
import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime

from database_connection.database_connection import connect_to_database


def extract_linestarapp(sport):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data') 
    data_files = {}

    for site in ['fd', 'dk']:
        data_files[site] = []
        
        #pid's used to append new data
        with connect_to_database() as cur:
            cur.execute('SELECT event_id FROM {}_linestarapp_{}'.format(sport, site))
            pids = set(x[0] for x in cur.fetchall())

        #loop thru bucket and extract data
        for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format(sport, 'linestarapp', site)):
        
            #skip objects if folder or projection data
            if obj.key[-1] == '/':
                continue
            
            #check if object is projection
            projections = True if 'projections' in obj.key else False
            
            #if file pid not in rds pid keys or file is projections, pull file, else continue        
            pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
            if pid in pids and not projections:
                continue
            else:
                file = s3.Object('my-dfs-data', obj.key)
                data = file.get()['Body'].read()
                data = json.loads(data)     
                data['projections'] = projections
                data_files[site].append(data)
                
    return data_files 
    

def etl_sportsline(sport):
    #initialize bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    data_files = {}
    
    links = []
    cols = ['link_pro', 'link_lead', 'link_bet']
    tables = [
        '{}_sportsline_pro',
        '{}_sportsline_lead',
        '{}_sportsline_bet'
    ]
    
    #pid's used to append new data
    with connect_to_database() as cur:
        for col, table in zip(cols, tables):
            cur.execute('SELECT DISTINCT {} FROM {}'.format(col, table))
            [links.append(link[0]) for link in cur.fetchall()]
    
    #loop thru bucket and extract data
    for obj in bucket.objects.filter(Prefix='{}/{}/'.format(sport, 'sportsline')):
        #skip objects if folder
        if obj.key[-1] == '/':
            continue
        
        #if file pid not in rds pid keys, pull file, else continue        
        link = obj.key.split('/')[-1]
        
        if link in links:
            continue
        else:
            file = s3.Object('my-dfs-data', obj.key)
            data = file.get()['Body'].read()
            data = json.loads(data)

        # if 'dfs-pro' in link:
        #     data = _transform_sportsline_pro(data, link)
        #     for row in data:
        #         _insert_sportsline_pro(row)
                
        # elif 'surprising-picks' in link and sport == 'pga': 
        #     data = _extract_sportsline_lead(data)
        #     data = _transform_sportsline_lead(data, link)
        #     for row in data:
        #         _insert_sportsline_lead(row)
        
        ### have to think about how different titles relate to different sports

        



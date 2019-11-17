#pull s3 & prep into rds
import psycopg2
import boto3
import json

from pga.etl.extract_linestarapp import LinestarappETL
from pga.etl.extract_sportsline import _sportsline_dfs_pro_data
from pga.etl.extract_sportsline import _sportsline_picks_data
from pga.etl.transform_data import *
from pga.etl.load_data import _insert_sportsline_dfs_pro
from pga.etl.load_data import _insert_sportsline_picks
from pga.etl.load_data import insert_linestarapp
from pga.etl.combine_data import create_table
from pga.etl.sql_queries import *


class ETL:
    def __init__(self, source, cursor):
        self.source == source
        self.cur = cursor

        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket('my-dfs-data')    

    
    def etl_linestarapp(cur, sport):
        for site in ['fd', 'dk']:
        
            #pid's used to append new data
            cur.execute('SELECT event_id FROM {}_linestarapp_{}'.format(sport, site))
            pids = set(x[0] for x in cur.fetchall())
            
            #initialize bucket
            s3 = boto3.resource('s3')
            bucket = s3.Bucket('my-dfs-data')
            
            #initialize extraction
            extract = LinestarappETL()
            
            # loop thru bucket and extract data
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
                
                #transform file into usable dictionary
                data_cache = extract.transform_linestarapp(data, projections)
        
                #load dict into rds as new record
                for player_id in data_cache[pid]:
                    insert_linestarapp(cur, data_cache[pid][player_id], pid, sport, site, projections)    
    

def etl_sportsline(cur, sport):
    #initialize bucket
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    links = []
    cols = ['link_pro', 'link_picks']
    tables = [
        'pga_sportsline_dfs_pro',
        'pga_sportsline_picks'
    ]
    for col, table in zip(cols, tables):
        cur.execute('SELECT DISTINCT {} FROM {}'.format(col, table))
        [links.append(link[0]) for link in cur.fetchall()]
    
    # loop thru bucket and extract data
    for obj in bucket.objects.filter(Prefix='{}/{}/'.format('pga', 'sportsline')):
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
                
        if 'surprising-picks' in link: 
            data = _sportsline_picks_data(data)
            data = transform_sportsline_picks(data, link)
            for row in data:
                _insert_sportsline_picks(cur, row)
            
        elif 'dfs-pro' in link:
            data = _sportsline_dfs_pro_data(data)
            data = transform_sportsline_dfs_pro(data, link)
            for row in data:
                _insert_sportsline_dfs_pro(cur, row)
            

def etl_linestarapp(cur, sport):
    for site in ['fd', 'dk']:
    
        #pid's used to append new data
        cur.execute('SELECT event_id FROM {}_linestarapp_{}'.format(sport, site))
        pids = set(x[0] for x in cur.fetchall())
        
        #initialize bucket
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-dfs-data')
        
        #initialize extraction
        extract = LinestarappETL()
        
        # loop thru bucket and extract data
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
            
            #transform file into usable dictionary
            data_cache = extract.transform_linestarapp(data, projections)
    
            #load dict into rds as new record
            for player_id in data_cache[pid]:
                insert_linestarapp(cur, data_cache[pid][player_id], pid, sport, site, projections)


def etl(cursor, sport):
    #etl_sportsline(cursor, sport)
    etl_linestarapp(cursor, sport)


if __name__ == '__main__':
    pass

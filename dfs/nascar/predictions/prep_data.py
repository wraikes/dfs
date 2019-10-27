import json
import boto3
import pandas as pd
import pickle
import numpy as np

from database_connection import connect_to_database
from etl_linestarapp import LinestarappETL
from etl_sportsline import _sportsline_leaderboard_data
from etl_sportsline import _sportsline_betting_data
from etl_sportsline import _sportsline_dfs_pro_data

def load_linestarapp():
    #load relevant data for projections
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format('nascar', 'linestarapp', 'fd')):
    #skip objects if not projection data
        if 'projections' not in obj.key:
            continue
        
        #pull file        
        file = s3.Object('my-dfs-data', obj.key)
        data = file.get()['Body'].read()
        data = json.loads(data)
        
        #transform file into usable dictionary
        etl = LinestarappETL()
        data_cache = etl.transform_linestarapp(data)

        df = pd.DataFrame.from_dict({(i,j): data_cache[i][j] 
                           for i in data_cache.keys() 
                           for j in data_cache[i].keys()},
                       orient='index')
                       
        df.columns = [
                
        ]
                       
        return df



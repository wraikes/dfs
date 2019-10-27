import pandas as pd
import numpy as np
import boto3

def prep_data():
    bucket = 'my-dfs-data'
    file_name = "training_data/nascar.csv"

    s3 = boto3.client('s3') 
    obj = s3.get_object(Bucket= bucket, Key= file_name) 
    df = pd.read_csv(obj['Body']) 

    cols = [x for x in df.count().index if df.count()[x] == 0]
    df = df.drop(columns=cols)
    df = df.fillna(0)
    
    df['names'] = df['name']
    df = pd.get_dummies(df, columns=['names', 'surface', 'restrictor_plate'])
    
    drop_cols = [
        'primary_id',
        'race_id',
        's',
        'race_date',
        'player_id',
        'pos',
        'gid',
        'ss',
        'stat',
        'is_',
        'notes',
        'floor',
        'ceil',
        'conf',
        'ptid',
        'otid',
        'htid',
        'opprank',
        'opptotal',
        'dspid',
        'dgid',
        'lock',
        'id',
        'salaryid',
        'owned', #might be projected owned
        'link_lead',
        'title_lead',
        'date_x',
        'pos_lead',
        'link_pro',
        'title_pro',
        'date_y',
        'link_betting',
        'title_betting',
        'date'
    ]
    
    return df.drop(columns=drop_cols)
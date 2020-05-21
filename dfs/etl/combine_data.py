import boto3
import pandas as pd
from io import StringIO 

from database_connection.database_connection import connect_to_database

def pull_tables(sport, site):
    
    with connect_to_database() as cur:
        cur.execute("SELECT * FROM {}_linestarapp_{}".format(sport, site))
        linestar = pd.DataFrame(
            cur.fetchall(), 
            columns=[desc[0] for desc in cur.description]
        )
        
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    csv_buffer = StringIO()
    linestar.to_csv(csv_buffer, index=False)
    s3.Object(bucket.name, '{}/modeling/final_data_{}_linestarapp.csv'.format(sport, site)).put(Body=csv_buffer.getvalue())

    return linestar


def clean_data(df, sport):
    if sport == 'nascar':
        cols = [
            'practice_best_lap_time_1', 
            'practice_best_lap_speed_1', 
            'finished_4', 
            'wins_4', 
            'top_5s_4', 
            'top_10s_4', 
            'races_4'
        ]
        
        for col in cols:
            df[col] = pd.to_numeric(df[col])
        
        df['practice_best_lap_time_rank'] = df.groupby('event_id')['practice_best_lap_time_1'].rank()
        df['practice_best_lap_speed_rank'] = df.groupby('event_id')['practice_best_lap_speed_1'].rank()
        percent_cols = ['finished_4', 'wins_4', 'top_5s_4', 'top_10s_4']
        
    elif sport == 'pga':
        cols = []
        
        for col in cols:
            df[col] = pd.to_numeric(df[col])
        

    return df
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



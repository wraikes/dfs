#pull s3 & prep into rds
import psycopg2
import boto3
import json

from etl.extract import *
from etl.transform import *
from etl.load import *

def etl(sport, source):
    if source == 'linestarapp':
        
        data = extract_linestarapp(sport)        
        data = transform_linestarapp(data)        
        insert_linestarapp(data, sport)
        
    elif source == 'sportsline':
        data = extract_sportsline(sport)        
        data = transform_sportsline(data)        
        insert_sportsline(data, sport)
    
    else:
        #source == nerd
        pass


if __name__ == '__main__':
    pass

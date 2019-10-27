import pandas as pd
import psycopg2
import configparser
import boto3
import numpy as np

#load all databases
#clean all databases for merge
#merge all databases into one pandas dataframe

from database_connection import connect_to_database

def load_linestarapp():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_linestarapp")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return transform_linestarapp(df)
    

def transform_linestarapp(df):
    tmp = df.copy()
    tmp['race_date'] = pd.to_datetime(pd.to_datetime(tmp['race_date'], utc=True).dt.date)

    return tmp
    

def load_sportsline_leaderboard():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_sportsline_leaderboard")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return transform_sportsline_leaderboard(df)


def transform_sportsline_leaderboard(df):
    tmp = df.copy()
    tmp['date'] = pd.to_datetime(pd.to_datetime(tmp['date'], unit='s', utc=True).dt.date)
    
    new_df = pd.DataFrame(
            columns = [
                'link', 'title', 'date', 'name', 'pos'
            ]
    )
    for i in tmp.iterrows():
        for idx in i[1].index:
            if 'pos_' in idx and i[1][idx]:
                pos = idx.split('_')[1]
                new_row = {
                    'link': i[1]['link'],
                    'title': i[1]['title'],
                    'date': i[1]['date'],
                    'name': i[1][idx],
                    'pos': pos
                }
                new_df = new_df.append(new_row, ignore_index=True)
    
    new_df.columns = [x+'_lead' if 'name' not in x and 'date' not in x else x for x in new_df.columns ]
    
    return new_df.fillna(0)


def load_sportsline_betting():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_sportsline_betting")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return transform_sportsline_betting(df)

def transform_sportsline_betting(df):
    tmp = df.copy()
    tmp['date'] = pd.to_datetime(pd.to_datetime(tmp['date'], unit='s', utc=True).dt.date)
    
    new_df = pd.DataFrame(
        columns = [
            'link', 'title', 'date', 'name', 'pos', 'odds'
        ]
    )
    
    for i in tmp.iterrows():
        for idx in i[1].index:
            if 'pos_' in idx and 'odds' not in idx and i[1][idx]:
                pos = idx.split('_')[1]
                new_row = {
                    'link': i[1]['link'],
                    'title': i[1]['title'],
                    'date': i[1]['date'],
                    'name': i[1][idx],
                    'pos': pos,
                    'odds': odds(i[1][idx+'_odds'])
                }
                new_df = new_df.append(new_row, ignore_index=True)

    new_df.columns = [x+'_betting' if 'name' not in x and 'date' not in x else x for x in new_df.columns ]
    
    return new_df.fillna(0)

def load_sportsline_dfs_pro():
    cur = connect_to_database()
    
    cur.execute("SELECT * FROM nascar_sportsline_dfs_pro")
    df = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    
    return transform_sportsline_dfs_pro(df)

def transform_sportsline_dfs_pro(df):
    tmp = df.copy()
    tmp['date'] = pd.to_datetime(pd.to_datetime(tmp['date'], unit='s', utc=True).dt.date)

    new_df = pd.DataFrame(
            columns = [
                'link', 'title', 'date', 'name', 'dfs_pick_dk'
            ]
    )
    
    for i in tmp.iterrows():
        for idx in i[1].index:
            #only use dk picks
            if 'pick_dk' in idx and i[1][idx]:
                new_row = {
                    'link': i[1]['link'],
                    'title': i[1]['title'],
                    'date': i[1]['date'],
                    'name': i[1][idx],
                    'dfs_pick_dk': 1
                }
                new_df = new_df.append(new_row, ignore_index=True)

    new_df.columns = [x+'_pro' if 'name' not in x and 'date' not in x else x for x in new_df.columns ]

    return new_df.fillna(0)


def odds(odds):
    if odds:
        tmp = [int(x) for x in odds.split('-')]
        tmp = tmp[1] / sum(tmp)
    else:
        tmp = None
    return tmp


def combine_data(linestar, sportsline):
    new = pd.DataFrame()
    tol = pd.Timedelta('3 day')
    
    for name in linestar.name.unique():
        a = linestar[linestar.name==name].sort_values(by='race_date')
        b = sportsline[sportsline.name==name].sort_values(by='date')
        
        tmp = pd.merge_asof(left=a, right=b.drop(columns='name'),
                            left_on='race_date',
                            right_on='date',
                            direction='nearest',
                            tolerance=tol
                            )
        
        new = new.append(tmp)
    
    return new
    
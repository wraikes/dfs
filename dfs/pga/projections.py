import pickle
import boto3
import pandas as pd
import numpy as np
import json

from pga.predictions.optimizer import Optimizer
from pga.etl.extract_linestarapp import LinestarappETL


def get_lineup(cur, site):
    #load relevant data for projections
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format('pga', 'linestarapp', site)):
        #skip objects if not projection data
        if 'projections' not in obj.key:
            continue
        
        #pull file        
        file = s3.Object('my-dfs-data', obj.key)
        data = file.get()['Body'].read()
        data = json.loads(data)
        
    # file = s3.Object('my-dfs-data', 'nascar/linestarapp/{}_272.json'.format(site))
    # data = file.get()['Body'].read()
    # data = json.loads(data)
    
    #transform file into usable dictionary
    etl = LinestarappETL()
    line = etl.transform_linestarapp(data)
    line = pd.DataFrame.from_dict(
        {(i,j): line[i][j] for i in line.keys() for j in line[i].keys()},
        orient='index'
    ).reset_index()
    
    line.columns = [
        'primary_id', 'pga_id', 's', 'player_id', 'name', 'pos', 'salary', 'gid', 'gi', 'pga_date', 
        'ppg', 'pp', 'ps', 'ss', 'stat', 'is_', 'notes', 'floor', 'ceil', 'conf', 'ptid', 'otid', 
        'htid', 'oe', 'opprank', 'opptotal', 'dspid', 'dgid', 'img', 'pteam', 'hteam', 'oteam', 
        'lock', 'id', 'events', 'wins', 'top_5s', 'top_10s', 'avg_place', 'cuts_made',
        'cut_made', 'vegas_odds', 'vegas_value', 'events_1', 'wins_1', 'top_5s_1',
        'top_10s_1', 'avg_place_1', 'cuts_made_1', 'cut_made_1', 'events_2', 'wins_2',
        'top_5s_2', 'top_10s_2', 'avg_place_2', 'cuts_made_2', 'cut_made_2', 'gir',
        'driving_acc', 'driving_dist', 'putting_avg', 'scramble', 'events_3', 
        'avg_place_3', 'cuts_made_3', 'cut_made_3', 'gir_3', 'driving_acc_3', 
        'driving_dist_3', 'putting_avg_3', 'scramble_3', 'salaryid', 'owned', 'hatecount',
        'lovecount'
    ]
    
    line['pga_date'] = pd.to_datetime(pd.to_datetime(line['pga_date'], utc=True).dt.date)    
    
    cur.execute("SELECT * FROM pga_sportsline_picks")
    picks = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    picks = picks[picks.date_picks == picks.date_picks.max()]
    
    cur.execute("SELECT * FROM pga_sportsline_dfs_pro")
    pro = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    pro = pro[pro.date_pro == pro.date_pro.max()]
    
    if pro['name'].iloc[0].startswith('D '):
        pro['name'] = pro['name'].str.replace('D ', '')
    
    
    df_0 = line.copy()
    df_1 = pd.merge(df_0, picks[['name', 'pos_picks']], how='left', on='name')
    df_2 = pd.merge(df_1, pro[['name', 'dfs_pick_dk']], how='left', on='name')
    df = df_2.copy()
        
    picks = df.pos_picks.max()
    
    df.loc[(df['pos_picks']).isnull(), 'pos_picks'] = picks

    df['names'] = df['name']
    df = pd.get_dummies(df, columns=['names'])

    obj = pickle.loads(s3.Bucket("my-dfs-data").Object("pga/modeling/model_{}.pkl".format(site)).get()['Body'].read())
    
    for col in ['', '_1', '_2', '_3']:
        max_ = df['avg_place'+col].max()
        df['avg_place'+col] = np.where(df['avg_place'+col]=='-', max_, df['avg_place'+col])
    
    for col in obj[1]:
        if col not in df.columns:
            df[col] = 0
        else:
            df[col] = pd.to_numeric(df[col])
    
    df.fillna(0, inplace=True)
    df['preds'] = obj[0].predict(df[obj[1]])

    #use optimizer for lineups
    opt = Optimizer(df, site)
    opt.solve()
    opt.get_lineup()

    return opt.lineup



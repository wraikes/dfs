import pickle
import boto3
import pandas as pd
import numpy as np
import json

from nascar.predictions.optimizer import Optimizer
from nascar.etl.extract_linestarapp import LinestarappETL


def get_lineup(cur, site):
    #load relevant data for projections
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    for obj in bucket.objects.filter(Prefix='{}/{}/{}_'.format('nascar', 'linestarapp', site)):
        #skip objects if not projection data
        if 'projections' not in obj.key:
            continue
        
        #pull file        
        file = s3.Object('my-dfs-data', obj.key)
        data = file.get()['Body'].read()
        data = json.loads(data)
        
#    file = s3.Object('my-dfs-data', 'nascar/linestarapp/{}_272.json'.format(site))
#    data = file.get()['Body'].read()
#    data = json.loads(data)
    
    #transform file into usable dictionary
    etl = LinestarappETL()
    line = etl.transform_linestarapp(data)
    line = pd.DataFrame.from_dict(
        {(i,j): line[i][j] for i in line.keys() for j in line[i].keys()},
        orient='index'
    )
    
    line.columns = [
    's', 'player_id', 'name', 'pos', 'salary', 'gid',
    'gi', 'date', 
    'ppg', 'pp', 'ps', 'ss', 'stat', 'is_', 'notes', 'floor', 'ceil', 'conf',
    'ptid', 'otid', 
    'htid', 'oe', 'opprank', 'opptotal', 'dspid', 'dgid', 'img', 'pteam', 
    'hteam', 'oteam', 
    'lock', 'id', 'races', 'note_pos', 'wins', 'top_fives', 'top_tens', 'avg_finish', 
    'laps_led_race', 'fastest_laps_race', 'avg_pass_diff', 'quality_passes_race', 
    'fppg', 'practice_laps', 'practice_best_lap_time', 'practice_best_lap_speed', 
    'qualifying_pos', 'qualifying_best_lap_time', 'qualifying_best_lap_speed', 
    'laps', 'miles', 'surface', 'restrictor_plate', 'cautions_race', 'races_3', 
    'finished', 'wins_3', 'top_5s', 'top_10s', 'avg_place', 'races_4', 'finished_4', 
    'wins_4', 'top_5s_4', 'top_10s_4', 'avg_place_4', 'salaryid', 'owned', 
    'hatecount', 'lovecount']
    
    line['date'] = pd.to_datetime(pd.to_datetime(line['date'], utc=True).dt.date)    
    
    cur.execute("SELECT * FROM nascar_sportsline_leaderboard")
    lead = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    lead = lead[lead.date_leaderboard == lead.date_leaderboard.max()]
    
    cur.execute("SELECT * FROM nascar_sportsline_betting")
    bet = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    bet = bet[bet.date_betting == bet.date_betting.max()]
    
    cur.execute("SELECT * FROM nascar_sportsline_pro")
    pro = pd.DataFrame(
        cur.fetchall(), 
        columns=[desc[0] for desc in cur.description]
    )
    pro = pro[pro.date_pro == pro.date_pro.max()]
    
    # if pro['name'].iloc[0].startswith('D '):
    #     pro['name'] = pro['name'].str.replace('D ', '')
    
    # pro['name'].iloc[0] = 'Martin Truex Jr.'
    # pro['name'].iloc[4] = 'Ricky Stenhouse Jr.'
    
    df_0 = line.copy()
    df_1 = pd.merge(df_0, lead[['name', 'pos_leaderboard']], how='left', on='name')
    df_2 = pd.merge(df_1, pro[['name', 'dfs_pick_dk']], how='left', on='name')
    df_3 = pd.merge(df_2, bet[['name', 'pos_betting', 'pos_odds_betting']], how='left', on='name')
    df = df_3.copy()
        
    betting = df.pos_betting.max()
    lead = df.pos_leaderboard.max()
    note_pos = df.note_pos.max()
    
    df.loc[(df['pos_betting']).isnull(), 'pos_betting'] = betting
    df.loc[(df['pos_betting']).isnull(), 'pos_odds_betting'] = 0
    df.loc[(df['pos_leaderboard']).isnull(), 'pos_leaderboard'] = lead
    df.loc[(df['note_pos']).isnull(), 'note_pos'] = note_pos

    df['names'] = df['name']
    df = pd.get_dummies(df, columns=['names'])
    df['qualifying_pos'] = np.where(df['qualifying_pos']=='-', 0, df['qualifying_pos'])
    
    obj = pickle.loads(s3.Bucket("my-dfs-data").Object("nascar/modeling/model_{}.pkl".format(site)).get()['Body'].read())
    
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



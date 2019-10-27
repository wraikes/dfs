import pickle
import json
import boto3
import pandas as pd
import numpy as np

from database_connection import connect_to_database
from prepdata import *
from etl_linestarapp import LinestarappETL
from optimizer import Optimizer

def main():
    #load relevant data for projections
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    cur = connect_to_database()
    
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
        line = etl.transform_linestarapp(data)
        line.columns = [
        's', 'player_id', 'name', 'pos', 'salary', 'gid',
        'gi', 'race_date', 
        'ppg', 'pp', 'ps', 'ss', 'stat', 'is_', 'notes', 'floor', 'ceil', 'conf',
        'ptid', 'otid', 
        'htid', 'oe', 'opprank', 'opptotal', 'dspid', 'dgid', 'img', 'pteam', 
        'hteam', 'oteam', 
        'lock', 'id', 'races', 'wins', 'top_fives', 'top_tens', 'avg_finish', 
        'laps_led_race', 'fastest_laps_race', 'avg_pass_diff', 'quality_passes_race', 
        'fppg', 'practice_laps', 'practice_best_lap_time', 'practice_best_lap_speed', 
        'qualifying_pos', 'qualifying_best_lap_time', 'qualifying_best_lap_speed', 
        'laps', 'miles', 'surface', 'restrictor_plate', 'cautions_race', 'races_3', 
        'finished', 'wins_3', 'top_5s', 'top_10s', 'avg_place', 'races_4', 'finished_4', 
        'wins_4', 'top_5s_4', 'top_10s_4', 'avg_place_4', 'salaryid', 'owned', 
        'hatecount', 'lovecount']
        
    line['race_date'] = pd.to_datetime(pd.to_datetime(line['race_date'], utc=True).dt.date)    
    lead = load_sportsline_leaderboard()
    lead = lead[lead.date == lead.date.max()]
    bet = load_sportsline_betting()
    bet = bet[bet.date == bet.date.max()]
    pro = load_sportsline_dfs_pro()
    pro = pro[pro.date == pro.date.max()]
    
    df_0 = line.copy()
    df_1 = combine_data(df_0, lead)
    df_2 = combine_data(df_1, pro)
    df_3 = combine_data(df_2, bet)
    df = df_3.copy()
    for i in df.columns:
        print(i)
        
    #load model & make predictions
    df = df.fillna(0)
    
    df['names'] = df['name']
    df = pd.get_dummies(df, columns=['names', 'surface', 'restrictor_plate'])
    df['qualifying_pos'] = np.where(df['qualifying_pos']=='-', 0, df['qualifying_pos'])
    
    obj = pickle.loads(s3.Bucket("my-dfs-data").Object("modeling/nascar.pkl").get()['Body'].read())
    for col in obj[1]:
        if col not in df.columns:
            df[col] = 0
    #obj = s3.get_object(Bucket=bucket, Key='nascar/modeling/nascar.pkl') 
    df['preds'] = obj[0].predict(df[obj[1]])
    
    #use optimizer for lineups
    opt = Optimizer(df)
    opt.solve()
    opt.get_lineup()
    print(opt.lineup)
    return opt.lineup

if __name__ == '__main__':
    main()


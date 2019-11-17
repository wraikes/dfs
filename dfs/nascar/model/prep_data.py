import pandas as pd
import numpy as np

def prep_data(df):

    drop_cols = [
        'laps',
        'miles',
        'primary_id',
        'event_id',
        's',
        'player_id',
        'pos',
        'gid',
        'gi',
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
        'oe',
        'opprank',
        'opptotal',
        'dspid',
        'dgid',
        'img',
        'pteam',
        'hteam',
        'oteam',
        'lock',
        'id',
        'salaryid',
        'owned',
        'lovecount',
        'hatecount',
        'link_leaderboard',
        'title_leaderboard',
        'date_leaderboard',
        'link_pro',
        'title_pro',
        'date_pro',
        'link_betting',
        'title_betting',
        'date_betting',
        'surface',
        'restrictor_plate',
    ]
    
    df['names'] = df['name']
    df = df.drop(columns=drop_cols)
    df = pd.get_dummies(df, columns=['names'])
    df['dfs_pick_dk'] = df['dfs_pick_dk'].fillna(0)
    
    for col in df.columns:
        if col != 'name' and col != 'date':
            df[col] = pd.to_numeric(df[col])

    df = fill_na(df)

    df['best_lap_time_pos'] = None
    df['best_lap_speed_pos'] = None
    df['best_lap_time_pos_diff'] = None
    df['best_lap_speed_pos_diff'] = None
    
    df['best_lap_time_diff'] = df['practice_best_lap_time'] - df['qualifying_best_lap_time']
    df['best_lap_speed_diff'] = df['practice_best_lap_speed'] - df['qualifying_best_lap_speed']
    
    for date in df.date.unique():
        df.loc[df.date==date, 'best_lap_time_pos'] = df.loc[df.date==date, 'practice_best_lap_time'].rank()
        df.loc[df.date==date, 'best_lap_speed_pos'] = df.loc[df.date==date, 'practice_best_lap_speed'].rank()
        df.loc[df.date==date, 'best_lap_time_pos_diff'] = df.loc[df.date==date, 'practice_best_lap_time'] - df.loc[df.date==date, 'practice_best_lap_time'].min()
        df.loc[df.date==date, 'best_lap_speed_pos_diff'] = df.loc[df.date==date, 'practice_best_lap_speed'] - df.loc[df.date==date, 'practice_best_lap_speed'].min()
    
    for col in df.columns:
        if 'names_' in col:
            df[col] = df[col] * df['cautions_race']
    
    df['interaction'] = df['qualifying_pos'] * df['best_lap_time_pos_diff']
    
    return df.drop(columns=['date', 'cautions_race'])


def fill_na(df):
    bet_grp = df.groupby('name').pos_betting.mean()
    odds_grp = df.groupby('name').pos_odds_betting.mean()
    lead_grp = df.groupby('name').pos_leaderboard.mean()
    note = df.groupby('name').note_pos.mean()    
    
    for date in df.date.unique():
        tmp = df[df.date==date]
        
        betting = tmp.pos_betting.max()
        lead = tmp.pos_leaderboard.max()
        note_pos = tmp.note_pos.max()
        
        if not np.isnan(betting):
            df.loc[(df['date']==date)&(df['pos_betting']).isnull(), 'pos_betting'] = betting
            df.loc[(df['date']==date)&(df['pos_betting']).isnull(), 'pos_odds_betting'] = 0
        else:
            for name in tmp.name.unique():
                df.loc[(df['date']==date)&(df['name']==name), 'pos_betting'] = bet_grp[name]
                df.loc[(df['date']==date)&(df['name']==name), 'pos_odds_betting'] = odds_grp[name]
            
        if not np.isnan(lead):
            df.loc[(df['date']==date)&(df['pos_leaderboard']).isnull(), 'pos_leaderboard'] = lead
        else:
            for name in tmp.name.unique():
                df.loc[(df['date']==date)&(df['name']==name), 'pos_leaderboard'] = lead_grp[name]
                
        if not np.isnan(note_pos):
            df.loc[(df['date']==date)&(df['note_pos']).isnull(), 'note_pos'] = note_pos
        else:
            for name in tmp.name.unique():
                df.loc[(df['date']==date)&(df['name']==name), 'note_pos'] = note[name]
            
    return df

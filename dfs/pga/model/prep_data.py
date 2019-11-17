import pandas as pd
import numpy as np

def prep_data(df):

    drop_cols = [
        'primary_id',
        'pga_id',
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
        'link_picks',
        'title_picks',
        'date_picks',
        'link_pro',
        'title_pro',
        'date_pro'
    ]
    
    df['names'] = df['name']
    df = df.drop(columns=drop_cols)
    df = pd.get_dummies(df, columns=['names'])
    df['dfs_pick_dk'] = df['dfs_pick_dk'].fillna(0)
    
    for col in df.columns:
        if col != 'name' and col != 'pga_date':
            df[col] = pd.to_numeric(df[col])

    df = fill_na(df)
    
    return df.drop(columns=['pga_date'])


def fill_na(df):
    pick_grp = df.groupby('name').pos_picks.mean()
    
    for date in df.pga_date.unique():
        tmp = df[df.pga_date==date]
        
        pick = tmp.pos_picks.max()

        if not np.isnan(pick):
            df.loc[(df['pga_date']==date)&(df['pos_picks']).isnull(), 'pos_picks'] = pick
        else:
            for name in tmp.name.unique():
                df.loc[(df['pga_date']==date)&(df['name']==name), 'pos_picks'] = pick_grp[name]

    return df

import boto3
import pandas as pd
from io import StringIO 


def combine_data(linestar, sportsline):
    new = pd.DataFrame()
    tol = pd.Timedelta('3 day')
    
    if 'dfs_pick_dk' in sportsline.columns:
        if sportsline['name'][0].startswith('D '):
            sportsline['name'] = sportsline['name'].str.replace('D ', '')
    
    for name in linestar.name.unique():
        a = linestar[linestar.name==name].sort_values(by='date')
        
        date_col = [x for x in sportsline.columns if 'date_' in x][0]
        b = sportsline[sportsline.name==name].sort_values(by=date_col)
        
        a['date'] = pd.to_datetime(a['date'])
        b[date_col] = pd.to_datetime(b[date_col])

        tmp = pd.merge_asof(left=a, right=b.drop(columns=['name', 'primary_id']),
                            left_on='date',
                            right_on=date_col,
                            direction='nearest',
                            tolerance=tol
                            )
        
        new = new.append(tmp)

    return new


def create_table(cursor, site, save=False):
    cursor.execute("SELECT * FROM nascar_sportsline_leaderboard")
    lead = pd.DataFrame(
        cursor.fetchall(), 
        columns=[desc[0] for desc in cursor.description]
    )
    
    cursor.execute("SELECT * FROM nascar_sportsline_betting")
    betting = pd.DataFrame(
        cursor.fetchall(), 
        columns=[desc[0] for desc in cursor.description]
    )
    
    cursor.execute("SELECT * FROM nascar_sportsline_pro")
    pro = pd.DataFrame(
        cursor.fetchall(), 
        columns=[desc[0] for desc in cursor.description]
    )
    
    if site == 'fd':
        cursor.execute("SELECT * FROM nascar_linestarapp_fd")
        line = pd.DataFrame(
            cursor.fetchall(), 
            columns=[desc[0] for desc in cursor.description]
        )
    else:
        cursor.execute("SELECT * FROM nascar_linestarapp_dk")
        line = pd.DataFrame(
            cursor.fetchall(), 
            columns=[desc[0] for desc in cursor.description]
        )
        
    
    df_1 = combine_data(line, lead)
    df_2 = combine_data(df_1, pro)
    df_3 = combine_data(df_2, betting)

    if save:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-dfs-data')
        
        csv_buffer = StringIO()
        df_3.to_csv(csv_buffer, index=False)
        s3.Object(bucket.name, 'nascar/modeling/final_data_{}.csv'.format(site)).put(Body=csv_buffer.getvalue())
    
        return df_3
    
    else:
        return df_3


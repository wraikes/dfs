import boto3
import pandas as pd
from io import StringIO 

from database_connection.database_connection import connect_to_database

def combine_data(linestar, sportsline):
    new = pd.DataFrame()
    tol = pd.Timedelta('3 day')
    
    if 'dfs_pick_dk' in sportsline.columns:
        if sportsline['name'][0].startswith('D '):
            sportsline['name'] = sportsline['name'].str.replace('D ', '')
    
    for name in linestar.name.unique():
        a = linestar[linestar.name==name].sort_values(by='pga_date')
        
        date_col = [x for x in sportsline.columns if 'date_' in x][0]
        b = sportsline[sportsline.name==name].sort_values(by=date_col)
        
        a['pga_date'] = pd.to_datetime(a['pga_date'])
        b[date_col] = pd.to_datetime(b[date_col])

        tmp = pd.merge_asof(left=a, right=b.drop(columns=['name', 'primary_id']),
                            left_on='pga_date',
                            right_on=date_col,
                            direction='nearest',
                            tolerance=tol
                            )
        
        new = new.append(tmp)

    return new


def create_dataframe(sport, site, save=False):
    
    with connect_to_database() as cur:
        # cursor.execute("SELECT * FROM pga_sportsline_picks")
        # picks = pd.DataFrame(
        #     cursor.fetchall(), 
        #     columns=[desc[0] for desc in cursor.description]
        # )
        
        # cursor.execute("SELECT * FROM pga_sportsline_dfs_pro")
        # pro = pd.DataFrame(
        #     cursor.fetchall(), 
        #     columns=[desc[0] for desc in cursor.description]
        # )
    
        cur.execute("SELECT * FROM {}_linestarapp_{}".format(sport, site))
        linestar = pd.DataFrame(
            cur.fetchall(), 
            columns=[desc[0] for desc in cur.description]
        )
        
    df = linestar.copy()
    #df_1 = combine_data(line, picks)
    #df_2 = combine_data(df_1, pro)

    if save:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('my-dfs-data')
        
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.Object(bucket.name, '{}/modeling/final_data_{}.csv'.format(sport, site)).put(Body=csv_buffer.getvalue())
    
        return df
    
    else:
        return df


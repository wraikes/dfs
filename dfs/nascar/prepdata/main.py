import boto3
from io import StringIO 

from prepdata import *

def main():
    betting = load_sportsline_betting()
    pro = load_sportsline_dfs_pro()
    lead = load_sportsline_leaderboard()
    line = load_linestarapp()

    df_0 = line.copy()
    df_1 = combine_data(df_0, lead)
    df_2 = combine_data(df_1, pro)
    df_3 = combine_data(df_2, betting)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    
    csv_buffer = StringIO()
    df_3.to_csv(csv_buffer, index=False)
    s3.Object(bucket.name, 'training_data/nascar').put(Body=csv_buffer.getvalue())


if __name__ == '__main__':
    main()

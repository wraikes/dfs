import json
import bs4
import boto3
import requests
import configparser

#PID earliest is 209

cfg = configparser.ConfigParser()
cfg.read('my_config.ini')

dbname = cfg['PGCONNECT']['dbname']
host = cfg['PGCONNECT']['host']
port = cfg['PGCONNECT']['port']
user = cfg['PGCONNECT']['user']
password = cfg['PGCONNECT']['password']

try:
    conn = psycopg2.connect(
        dbname=dbname, 
        host=host, 
        port=port, 
        user=user, 
        password=password
    )
    conn.autocommit = True

except:
    print('Unable to connect to the database.')
    
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS nascar_linestar')
cur.execute('\
    CREATE TABLE IF NOT EXISTS nascar_linestar ( \
    primary_key SERIAL PRIMARY KEY, \
    



    player_name VARCHAR, \
    likes INT, \
    inj VARCHAR, \
    pos VARCHAR, \
    salary NUMERIC, \
    team VARCHAR, \
    opp VARCHAR, \
    rest INT, \
    ps NUMERIC, \
    usg NUMERIC, \
    per NUMERIC, \
    opp_pace NUMERIC, \
    opp_deff NUMERIC, \
    opp_dvp NUMERIC, \
    l2_fga NUMERIC, \
    l5_fga NUMERIC, \
    s_fga NUMERIC, \
    l2_min NUMERIC, \
    l5_min NUMERIC, \
    s_min NUMERIC, \
    l5_fp NUMERIC, \
    s_fp NUMERIC, \
    floor_fp NUMERIC, \
    ceil_fp NUMERIC, \
    proj_min NUMERIC, \
    proj_fp NUMERIC, \
    proj_val NUMERIC, \
    actual_min NUMERIC, \
    actual_fp NUMERIC, \
    actual_val NUMERIC, \
    date VARCHAR \
    )'
)
json_data = requests.get('https://www.linestarapp.com/Projections/Sport/NAS/Site/FanDuel/PID/209')





for i in range(209, 257):
    html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport=9&site=2&periodId={}'.format(i)
    page = requests.get(html).content.decode()   
    json_data = json.loads(page)

table_values = {}

for i in range(len(json_data['MatchupData'])):
    columns = json_data['MatchupData'][i]['Columns']
    
    for player in range(len(json_data['MatchupData'][i]['PlayerMatchups'])):
        data = json_data['MatchupData'][i]['PlayerMatchups'][player]
        table_values[data['PlayerId']] = dict(zip(cols, data['Values']))
        
ownership_values = []

for player in range(len(json_data['Ownership']['Salaries'])):
    ownership_values.append(json_data['Ownership']['Salaries'][player])

for i in ownership_values:
    player_id = ownership_values[i]['PID']
    ownership_values[i].append(table_values[player_id])
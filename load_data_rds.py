import psycopg2
import boto3
import configparser
from scrape_nascar_data import site_load

cfg = configparser.ConfigParser()
cfg.read('tmp.ini')

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
    s INT, \
    pid INT, \
    name VARCHAR, \
    pos VARCHAR, \
    sal NUMERIC, \
    gid NUMERIC, \
    gi VARCHAR, \
    gt VARCHAR, \
    ppg NUMERIC, \
    pp NUMERIC, \
    ps NUMERIC, \
    ss NUMERIC, \
    stat NUMERIC, \
    is NUMERIC, \
    notes VARCHAR, \
    floor NUMERIC, \
    ceil NUMERIC, \
    conf NUMERIC, \
    ptid NUMERIC, \
    otid NUMERIC, \
    htid NUMERIC, \
    oe VARCHAR, \
    opprank NUMERIC, \
    opptotal NUMERIC, \
    dspid NUMERIC, \
    dgid NUMERIC, \
    img VARCHAR, \
    pteam VARCHAR, \
    hteam VARCHAR, \
    oteam VARCHAR, \
    lock NUMERIC, \
    id NUMERIC, \
    races NUMERIC, \
    wins NUMERIC, \
    top_fives NUMERIC, \
    top_tens NUMERIC, \
    avg_finish NUMERIC, \
    laps_led_race NUMERIC, \
    fastest_laps_race NUMERIC, \
    avg_pass_diff NUMERIC, \
    quality_passes_race NUMERIC, \
    fppg NUMERIC, \
    practice_laps NUMERIC, \
    practice_best_lap_time NUMERIC, \
    practice_best_lap_speed NUMERIC, \
    qualifying_pos NUMERIC, \
    qualifying_best_lap_time NUMERIC, \
    qualifying_best_lap_speed NUMERIC, \
    laps NUMERIC, \
    miles NUMERIC, \
    surface VARCHAR, \
    restrictor_plate VARCHAR, \
    cautions_race NUMERIC, \
    finished NUMERIC, \
    top_5s NUMERIC, \
    top_10s NUMERIC, \
    avg_place NUMERIC
    )'
)



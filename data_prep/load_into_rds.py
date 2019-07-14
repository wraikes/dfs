#note, this is a candidate to load straight into dynamodb (json structure).
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
    is_ NUMERIC, \
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
    avg_place NUMERIC \
    )'
)

#for loop all website data
for i in range(209, 257):
    print(i)
    data = site_load(i)
    
    for row in data:
        cur.execute('INSERT INTO nascar_linestar \
            (s, pid, name, pos, sal, gid, gi, gt, \
            ppg, pp, ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, \
            htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, oteam, \
            lock, id, races, wins, top_fives, top_tens, avg_finish, \
            laps_led_race, fastest_laps_race, avg_pass_diff, quality_passes_race, \
            fppg, practice_laps, practice_best_lap_time, practice_best_lap_speed, \
            qualifying_pos, qualifying_best_lap_time, qualifying_best_lap_speed, \
            laps, miles, surface, restrictor_plate, cautions_race, finished, \
            top_5s, top_10s, avg_place) \
            VALUES (\
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s)',
            (
                row['S'],
                row['PID'],
                row['Name'],
                row['POS'],
                row['SAL'],
                row['GID'],
                row['GI'],
                row['GT'],
                row['PPG'],
                row['PP'],
                row['PS'],
                row['SS'],
                row['STAT'],
                row['IS'],
                row['Notes'],
                row['Floor'],
                row['Ceil'],
                row['Conf'],
                row['PTID'],
                row['OTID'],
                row['HTID'],
                row['OE'],
                row['OppRank'],
                row['OppTotal'],
                row['DSPID'],
                row['DGID'],
                row['IMG'],
                row['PTEAM'],
                row['HTEAM'],
                row['OTEAM'],
                row['Lock'],
                row['Id'],
                float(row['Races']),
                float(row['Wins']),
                float(row['Top Fives']),
                float(row['Top Tens']),
                float(row['Avg Finish']),
                float(row['Laps Led/Race']),
                float(row['Fastest Laps/Race']),
                float(row['Avg Pass Diff']),
                float(row['Quality Passes/Race']),
                float(row['FPPG']),
                float(row['Practice Laps']),
                float(row['Practice Best Lap Time']),
                float(row['Practice Best Lap Speed']),
                float(row['Qualifying Pos']) if row['Qualifying Pos'] != '-' else None,
                float(row['Qualifying Best Lap Time']),
                float(row['Qualifying Best Lap Speed']),
                float(row['Laps']),
                float(row['Miles']),
                row['Surface'],
                row['Restrictor Plate?'],
                float(row['Cautions/Race']),
                float(row['Finished']),
                float(row['Top 5s']),
                float(row['Top 10s']),
                float(row['Avg. Place'])
            )
        )
    

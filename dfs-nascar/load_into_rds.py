#note, this is a candidate to load straight into dynamodb (json structure).
import psycopg2
import boto3
import configparser
from nascar_lineups.scrape_nascar_data import NascarDataPull

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
    race_id INT, \
    s INT, \
    pid INT, \
    name VARCHAR, \
    pos VARCHAR, \
    salary NUMERIC, \
    gid NUMERIC, \
    gi VARCHAR, \
    race_date VARCHAR, \
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
    races_3 NUMERIC, \
    finished NUMERIC, \
    wins_3 NUMERIC, \
    top_5s NUMERIC, \
    top_10s NUMERIC, \
    avg_place NUMERIC, \
    races_4 NUMERIC, \
    finished_4 NUMERIC, \
    wins_4 NUMERIC, \
    top_5s_4 NUMERIC, \
    top_10s_4 NUMERIC, \
    avg_place_4 NUMERIC \
    )'
)

data_pull = NascarDataPull(train=True, pid=212)
data_pull.pull_json_data()
data_pull.extract_owner_data()
data_pull.extract_table_data()

for race_id in data_pull._final_data.keys():
    for player in data_pull._final_data[race_id].keys():
        
        cur.execute('INSERT INTO nascar_linestar (\
            race_id, s, pid, name, pos, salary, gid, gi, race_date, \
            ppg, pp, ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, \
            htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, oteam, \
            lock, id, races, wins, top_fives, top_tens, avg_finish, \
            laps_led_race, fastest_laps_race, avg_pass_diff, quality_passes_race, \
            fppg, practice_laps, practice_best_lap_time, practice_best_lap_speed, \
            qualifying_pos, qualifying_best_lap_time, qualifying_best_lap_speed, \
            laps, miles, surface, restrictor_plate, cautions_race, races_3, \
            finished, wins_3, top_5s, top_10s, avg_place, races_4, finished_4, \
            wins_4, top_5s_4, top_10s_4, avg_place_4 \
            ) VALUES (\
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
            %s, %s, %s, %s, %s, %s)',
            (
                race_id,
                data_pull._final_data[race_id][player]['S'],
                data_pull._final_data[race_id][player]['PID'],
                data_pull._final_data[race_id][player]['Name'],
                data_pull._final_data[race_id][player]['POS'],
                data_pull._final_data[race_id][player]['SAL'],
                data_pull._final_data[race_id][player]['GID'],
                data_pull._final_data[race_id][player]['GI'],
                data_pull._final_data[race_id][player]['GT'],
                data_pull._final_data[race_id][player]['PPG'],
                data_pull._final_data[race_id][player]['PP'],
                data_pull._final_data[race_id][player]['PS'],
                data_pull._final_data[race_id][player]['SS'],
                data_pull._final_data[race_id][player]['STAT'],
                data_pull._final_data[race_id][player]['IS'],
                data_pull._final_data[race_id][player]['Notes'],
                data_pull._final_data[race_id][player]['Floor'],
                data_pull._final_data[race_id][player]['Ceil'],
                data_pull._final_data[race_id][player]['Conf'],
                data_pull._final_data[race_id][player]['PTID'],
                data_pull._final_data[race_id][player]['OTID'],
                data_pull._final_data[race_id][player]['HTID'],
                data_pull._final_data[race_id][player]['OE'],
                data_pull._final_data[race_id][player]['OppRank'],
                data_pull._final_data[race_id][player]['OppTotal'],
                data_pull._final_data[race_id][player]['DSPID'],
                data_pull._final_data[race_id][player]['DGID'],
                data_pull._final_data[race_id][player]['IMG'],
                data_pull._final_data[race_id][player]['PTEAM'],
                data_pull._final_data[race_id][player]['HTEAM'],
                data_pull._final_data[race_id][player]['OTEAM'],
                data_pull._final_data[race_id][player]['Lock'],
                data_pull._final_data[race_id][player]['Id'],
                float(data_pull._final_data[race_id][player]['Races']),
                float(data_pull._final_data[race_id][player]['Wins']),
                float(data_pull._final_data[race_id][player]['Top Fives']),
                float(data_pull._final_data[race_id][player]['Top Tens']),
                float(data_pull._final_data[race_id][player]['Avg Finish']),
                float(data_pull._final_data[race_id][player]['Laps Led/Race']),
                float(data_pull._final_data[race_id][player]['Fastest Laps/Race']),
                float(data_pull._final_data[race_id][player]['Avg Pass Diff']),
                float(data_pull._final_data[race_id][player]['Quality Passes/Race']),
                float(data_pull._final_data[race_id][player]['FPPG']),
                float(data_pull._final_data[race_id][player]['Practice Laps']),
                float(data_pull._final_data[race_id][player]['Practice Best Lap Time']),
                float(data_pull._final_data[race_id][player]['Practice Best Lap Speed']),
                float(data_pull._final_data[race_id][player]['Qualifying Pos']) if data_pull._final_data[race_id][player]['Qualifying Pos'] != '-' else None,
                float(data_pull._final_data[race_id][player]['Qualifying Best Lap Time']),
                float(data_pull._final_data[race_id][player]['Qualifying Best Lap Speed']),
                float(data_pull._final_data[race_id][player]['Laps']),
                float(data_pull._final_data[race_id][player]['Miles']),
                data_pull._final_data[race_id][player]['Surface'],
                data_pull._final_data[race_id][player]['Restrictor Plate?'],
                float(data_pull._final_data[race_id][player]['Cautions/Race']),
                float(data_pull._final_data[race_id][player]['Races_3']),
                float(data_pull._final_data[race_id][player]['Finished']),
                float(data_pull._final_data[race_id][player]['Wins_3']),
                float(data_pull._final_data[race_id][player]['Top 5s']),
                float(data_pull._final_data[race_id][player]['Top 10s']),
                float(data_pull._final_data[race_id][player]['Avg. Place']),
                float(data_pull._final_data[race_id][player]['Races_4']),
                float(data_pull._final_data[race_id][player]['Finished_4']),
                float(data_pull._final_data[race_id][player]['Wins_4']),
                float(data_pull._final_data[race_id][player]['Top 5s_4']),
                float(data_pull._final_data[race_id][player]['Top 10s_4']),
                float(data_pull._final_data[race_id][player]['Avg. Place_4'])
            )
        )

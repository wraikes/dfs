#load s3 data into respective rds databases
import boto3
import pandas as pd
import numpy as np
import json
import configparser
import psycopg2
import sys

cfg = configparser.ConfigParser()
cfg.read('database.ini')

dbname = cfg['PGCONNECT']['dbname']
host = cfg['PGCONNECT']['host']
port = cfg['PGCONNECT']['port']
user = cfg['PGCONNECT']['user']
password = cfg['PGCONNECT']['password']

###################
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

def create_nascar_tables():
    
    cur.execute('DROP TABLE IF EXISTS nascar_linestarapp')
    cur.execute('DROP TABLE IF EXISTS nascar_sportsline')
    
    cur.execute('\
        CREATE TABLE IF NOT EXISTS nascar_linestarapp ( \
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
        avg_place_4 NUMERIC, \
        owned NUMERIC, \
        salaryid NUMERIC, \
        lovecount NUMERIC, \
        hatecount NUMERIC \
        )'
    )
    
    cur.execute('\
        CREATE TABLE IF NOT EXISTS nascar_sportsline ( \
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
        avg_place_4 NUMERIC, \
        owned NUMERIC, \
        salaryid NUMERIC, \
        lovecount NUMERIC, \
        hatecount NUMERIC \
        )'
    )

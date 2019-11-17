#drop tables
drop_linestarapp_table = '''
    DROP TABLE IF EXISTS {}_linestarapp_{}
'''
drop_sportsline_table = '''
    DROP TABLE IF EXISTS {}_sportsline_{}
'''

#sportsline articles from dfs pro
sportsline_pro_create_table = '''
    CREATE TABLE IF NOT EXISTS {}_sportsline_pro (
        primary_id SERIAL PRIMARY KEY,
        link_pro VARCHAR,
        title_pro VARCHAR,
        date_pro VARCHAR,
        name VARCHAR,
        dfs_pick_dk INT
    )
'''

#sportsline articles that have rankings only
sportsline_leaderboard_create_table = '''
    CREATE TABLE IF NOT EXISTS {}_sportsline_leaderboard (
        primary_id SERIAL PRIMARY KEY,
        link_leaderboard VARCHAR,
        title_leaderboard VARCHAR,
        date_leaderboard VARCHAR,
        name VARCHAR,
        pos_leaderboard INT
    )
'''

#sportsline articles that have rankings and odds
sportsline_betting_create_table = '''
    CREATE TABLE IF NOT EXISTS {}_sportsline_betting (
        primary_id SERIAL PRIMARY KEY,
        link_betting VARCHAR,
        title_betting VARCHAR,
        date_betting VARCHAR,
        name VARCHAR,
        pos_betting INT,
        pos_odds_betting FLOAT
    )
'''

#nascar linestarapp
nascar_linestarapp_create_table = '''
    CREATE TABLE IF NOT EXISTS nascar_linestarapp_{} ( 
        primary_id SERIAL PRIMARY KEY, 
        event_id INT, 
        s INT, 
        player_id INT, 
        name VARCHAR, 
        pos VARCHAR, 
        salary NUMERIC, 
        gid NUMERIC, 
        gi VARCHAR, 
        date VARCHAR, 
        ppg NUMERIC, 
        pp NUMERIC, 
        ps NUMERIC, 
        ss NUMERIC, 
        stat NUMERIC, 
        is_ NUMERIC, 
        notes VARCHAR, 
        floor NUMERIC, 
        ceil NUMERIC, 
        conf NUMERIC, 
        ptid NUMERIC, 
        otid NUMERIC, 
        htid NUMERIC, 
        oe VARCHAR, 
        opprank NUMERIC, 
        opptotal NUMERIC, 
        dspid NUMERIC, 
        dgid NUMERIC, 
        img VARCHAR, 
        pteam VARCHAR, 
        hteam VARCHAR, 
        oteam VARCHAR, 
        lock NUMERIC, 
        id NUMERIC, 
        races NUMERIC, 
        wins NUMERIC, 
        top_fives NUMERIC, 
        top_tens NUMERIC, 
        avg_finish NUMERIC, 
        laps_led_race NUMERIC, 
        fastest_laps_race NUMERIC, 
        avg_pass_diff NUMERIC, 
        quality_passes_race NUMERIC, 
        fppg NUMERIC, 
        practice_laps NUMERIC, 
        practice_best_lap_time NUMERIC, 
        practice_best_lap_speed NUMERIC, 
        qualifying_pos NUMERIC, 
        qualifying_best_lap_time NUMERIC, 
        qualifying_best_lap_speed NUMERIC, 
        laps NUMERIC,
        miles NUMERIC, 
        surface VARCHAR, 
        restrictor_plate VARCHAR, 
        cautions_race NUMERIC, 
        races_3 NUMERIC, 
        finished NUMERIC, 
        wins_3 NUMERIC, 
        top_5s NUMERIC, 
        top_10s NUMERIC, 
        avg_place NUMERIC, 
        races_4 NUMERIC, 
        finished_4 NUMERIC, 
        wins_4 NUMERIC, 
        top_5s_4 NUMERIC, 
        top_10s_4 NUMERIC, 
        avg_place_4 NUMERIC, 
        salaryid NUMERIC, 
        owned NUMERIC, 
        hatecount NUMERIC, 
        lovecount NUMERIC,
        note_pos NUMERIC,
        projections VARCHAR
    )
'''

#pga linestarapp
pga_linestarapp_create_table = '''
    CREATE TABLE IF NOT EXISTS pga_linestarapp_{} ( 
        primary_id SERIAL PRIMARY KEY, 
        event_id INT, 
        s INT, 
        player_id INT, 
        name VARCHAR, 
        pos VARCHAR, 
        salary NUMERIC, 
        gid NUMERIC, 
        gi VARCHAR, 
        date VARCHAR, 
        ppg NUMERIC, 
        pp NUMERIC, 
        ps NUMERIC, 
        ss NUMERIC, 
        stat NUMERIC, 
        is_ NUMERIC, 
        notes VARCHAR, 
        floor NUMERIC, 
        ceil NUMERIC, 
        conf NUMERIC, 
        ptid NUMERIC, 
        otid NUMERIC, 
        htid NUMERIC, 
        oe VARCHAR, 
        opprank NUMERIC, 
        opptotal NUMERIC, 
        dspid NUMERIC, 
        dgid NUMERIC, 
        img VARCHAR, 
        pteam VARCHAR, 
        hteam VARCHAR, 
        oteam VARCHAR, 
        lock NUMERIC, 
        id NUMERIC, 
        events NUMERIC,
        wins NUMERIC,
        top_5s NUMERIC,
        top_10s NUMERIC,
        avg_place NUMERIC,
        cuts_made NUMERIC,
        cut_made NUMERIC,
        vegas_odds NUMERIC,
        vegas_value NUMERIC,
        events_1 NUMERIC,
        wins_1 NUMERIC,
        top_5s_1 NUMERIC,
        top_10s_1 NUMERIC,
        avg_place_1 NUMERIC,
        cuts_made_1 NUMERIC,
        cut_made_1 NUMERIC,
        events_2 NUMERIC,
        wins_2 NUMERIC,
        top_5s_2 NUMERIC,
        top_10s_2 NUMERIC,
        avg_place_2 NUMERIC,
        cuts_made_2 NUMERIC,
        cut_made_2 NUMERIC,
        gir NUMERIC,
        driving_acc NUMERIC,
        driving_dist NUMERIC,
        putting_avg NUMERIC,
        scramble NUMERIC,
        events_3 NUMERIC, 
        avg_place_3 NUMERIC,
        cuts_made_3 NUMERIC,
        cut_made_3 NUMERIC,
        gir_3 NUMERIC,
        driving_acc_3 NUMERIC, 
        driving_dist_3 NUMERIC,
        putting_avg_3 NUMERIC,
        scramble_3 NUMERIC,
        salaryid NUMERIC,
        owned NUMERIC,
        hatecount NUMERIC,
        lovecount NUMERIC,
        projections VARCHAR
    )
'''

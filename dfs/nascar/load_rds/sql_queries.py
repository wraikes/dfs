nascar_sportsline_dfs_pro_create_table = '''
    CREATE TABLE IF NOT EXISTS nascar_sportsline_dfs_pro (
        primary_id SERIAL PRIMARY KEY,
        link VARCHAR,
        title VARCHAR,
        date VARCHAR,
        dfs_pick_dk_1 VARCHAR,
        dfs_pick_dk_2 VARCHAR,
        dfs_pick_dk_3 VARCHAR,
        dfs_pick_dk_4 VARCHAR,
        dfs_pick_dk_5 VARCHAR,
        dfs_pick_dk_6 VARCHAR,
        dfs_pick_fd_1 VARCHAR,
        dfs_pick_fd_2 VARCHAR,
        dfs_pick_fd_3 VARCHAR,
        dfs_pick_fd_4 VARCHAR,
        dfs_pick_fd_5 VARCHAR
    )
'''

nascar_sportsline_dfs_pro_insert = '''
    INSERT INTO nascar_sportsline_dfs_pro (
        link, title, date, dfs_pick_dk_1, dfs_pick_dk_2, dfs_pick_dk_3,
        dfs_pick_dk_4, dfs_pick_dk_5, dfs_pick_dk_6, dfs_pick_fd_1,
        dfs_pick_fd_2, dfs_pick_fd_3, dfs_pick_fd_4, dfs_pick_fd_5
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
'''

nascar_sportsline_betting_create_table = '''
    CREATE TABLE IF NOT EXISTS nascar_sportsline_betting (
        primary_id SERIAL PRIMARY KEY,
        link VARCHAR,
        title VARCHAR,
        date VARCHAR,
        pos_1 VARCHAR,
        pos_2 VARCHAR,
        pos_3 VARCHAR,
        pos_4 VARCHAR,
        pos_5 VARCHAR,
        pos_6 VARCHAR,
        pos_7 VARCHAR,
        pos_8 VARCHAR,
        pos_9 VARCHAR,
        pos_10 VARCHAR,
        pos_11 VARCHAR,
        pos_12 VARCHAR,
        pos_13 VARCHAR,
        pos_14 VARCHAR,
        pos_15 VARCHAR,
        pos_16 VARCHAR,
        pos_17 VARCHAR,
        pos_18 VARCHAR,
        pos_19 VARCHAR,
        pos_20 VARCHAR,
        pos_1_odds VARCHAR,
        pos_2_odds VARCHAR,
        pos_3_odds VARCHAR,
        pos_4_odds VARCHAR,
        pos_5_odds VARCHAR,
        pos_6_odds VARCHAR,
        pos_7_odds VARCHAR,
        pos_8_odds VARCHAR,
        pos_9_odds VARCHAR,
        pos_10_odds VARCHAR,
        pos_11_odds VARCHAR,
        pos_12_odds VARCHAR,
        pos_13_odds VARCHAR,
        pos_14_odds VARCHAR,
        pos_15_odds VARCHAR,
        pos_16_odds VARCHAR,
        pos_17_odds VARCHAR,
        pos_18_odds VARCHAR,
        pos_19_odds VARCHAR,
        pos_20_odds VARCHAR
    )
'''

nascar_sportsline_betting_insert = '''
    INSERT INTO nascar_sportsline_betting (
        link, title, date, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8,
        pos_9, pos_10, pos_11, pos_12, pos_13, pos_14, pos_15, pos_16, pos_17,
        pos_18, pos_19, pos_20,
        pos_1_odds, pos_2_odds, pos_3_odds, pos_4_odds, pos_5_odds, pos_6_odds, 
        pos_7_odds, pos_8_odds, pos_9_odds, pos_10_odds, pos_11_odds, 
        pos_12_odds, pos_13_odds, pos_14_odds, pos_15_odds, pos_16_odds, 
        pos_17_odds, pos_18_odds, pos_19_odds, pos_20_odds
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
'''

nascar_sportsline_leaderboard_create_table = '''
    CREATE TABLE IF NOT EXISTS nascar_sportsline_leaderboard (
        primary_id SERIAL PRIMARY KEY,
        link VARCHAR,
        title VARCHAR,
        date VARCHAR,
        pos_1 VARCHAR,
        pos_2 VARCHAR,
        pos_3 VARCHAR,
        pos_4 VARCHAR,
        pos_5 VARCHAR,
        pos_6 VARCHAR,
        pos_7 VARCHAR,
        pos_8 VARCHAR,
        pos_9 VARCHAR,
        pos_10 VARCHAR,
        pos_11 VARCHAR,
        pos_12 VARCHAR,
        pos_13 VARCHAR,
        pos_14 VARCHAR,
        pos_15 VARCHAR,
        pos_16 VARCHAR,
        pos_17 VARCHAR,
        pos_18 VARCHAR,
        pos_19 VARCHAR,
        pos_20 VARCHAR,
        pos_21 VARCHAR,
        pos_22 VARCHAR,
        pos_23 VARCHAR,
        pos_24 VARCHAR,
        pos_25 VARCHAR,
        pos_26 VARCHAR,
        pos_27 VARCHAR,
        pos_28 VARCHAR,
        pos_29 VARCHAR,
        pos_30 VARCHAR,
        pos_31 VARCHAR,
        pos_32 VARCHAR,
        pos_33 VARCHAR,
        pos_34 VARCHAR,
        pos_35 VARCHAR,
        pos_36 VARCHAR,
        pos_37 VARCHAR,
        pos_38 VARCHAR,
        pos_39 VARCHAR,
        pos_40 VARCHAR
    )
'''

nascar_sportsline_leaderboard_insert = '''
    INSERT INTO nascar_sportsline_leaderboard (
        link, title, date, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8,
        pos_9, pos_10, pos_11, pos_12, pos_13, pos_14, pos_15, pos_16, pos_17,
        pos_18, pos_19, pos_20, pos_21, pos_22, pos_23, pos_24, pos_25, pos_26,
        pos_27, pos_28, pos_29, pos_30, pos_31, pos_32, pos_33, pos_34, pos_35,
        pos_36, pos_37, pos_38, pos_39, pos_40
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
'''

nascar_linestarapp_create_table = '''
    CREATE TABLE IF NOT EXISTS nascar_linestarapp ( 
        primary_id SERIAL PRIMARY KEY, 
        race_id INT, 
        s INT, 
        player_id INT, 
        name VARCHAR, 
        pos VARCHAR, 
        salary NUMERIC, 
        gid NUMERIC, 
        gi VARCHAR, 
        race_date VARCHAR, 
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
        owned NUMERIC, 
        salaryid NUMERIC, 
        lovecount NUMERIC, 
        hatecount NUMERIC 
    )
'''

nascar_linestarapp_insert = '''
    INSERT INTO nascar_linestarapp (
        race_id, s, player_id, name, pos, salary, gid, gi, race_date, 
        ppg, pp, ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, 
        htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, oteam, 
        lock, id, races, wins, top_fives, top_tens, avg_finish, 
        laps_led_race, fastest_laps_race, avg_pass_diff, quality_passes_race, 
        fppg, practice_laps, practice_best_lap_time, practice_best_lap_speed, 
        qualifying_pos, qualifying_best_lap_time, qualifying_best_lap_speed, 
        laps, miles, surface, restrictor_plate, cautions_race, races_3, 
        finished, wins_3, top_5s, top_10s, avg_place, races_4, finished_4, 
        wins_4, top_5s_4, top_10s_4, avg_place_4, owned, salaryid, lovecount, 
        hatecount 
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
'''


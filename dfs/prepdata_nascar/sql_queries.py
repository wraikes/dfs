nascar_linestarapp_create_table = '''
    CREATE TABLE IF NOT EXISTS linestarapp ( 
        primary_id SERIAL PRIMARY KEY, 
        race_id INT, 
        s INT, 
        pid INT, 
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


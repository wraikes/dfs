nascar_sportsline_dfs_pro_insert = '''
    INSERT INTO nascar_sportsline_dfs_pro (
        link_pro, title_pro, date_pro, name, dfs_pick_dk 
    ) VALUES (
        %s, %s, %s, %s, %s
    )
'''

nascar_sportsline_betting_insert = '''
    INSERT INTO nascar_sportsline_betting (
        link_betting, title_betting, date_betting, name, 
        pos_betting, pos_odds_betting
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
'''

nascar_sportsline_leaderboard_insert = '''
    INSERT INTO nascar_sportsline_leaderboard (
        link_leaderboard, title_leaderboard, date_leaderboard, name,
        pos_leaderboard
    ) VALUES (
        %s, %s, %s, %s, %s
    )
'''

nascar_linestarapp_insert_fd = '''
    INSERT INTO nascar_linestarapp_fd (
        race_id, s, player_id, name, pos, salary, gid, gi, race_date, 
        ppg, pp, ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, 
        htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, oteam, 
        lock, id, races, wins, top_fives, top_tens, avg_finish, 
        laps_led_race, fastest_laps_race, avg_pass_diff, quality_passes_race, 
        fppg, practice_laps, practice_best_lap_time, practice_best_lap_speed, 
        qualifying_pos, qualifying_best_lap_time, qualifying_best_lap_speed, 
        laps, miles, surface, restrictor_plate, cautions_race, races_3, 
        finished, wins_3, top_5s, top_10s, avg_place, races_4, finished_4, 
        wins_4, top_5s_4, top_10s_4, avg_place_4, salaryid, owned, hatecount, 
        lovecount, note_pos
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
'''

nascar_linestarapp_insert_dk = '''
    INSERT INTO nascar_linestarapp_dk (
        race_id, s, player_id, name, pos, salary, gid, gi, race_date, 
        ppg, pp, ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, 
        htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, oteam, 
        lock, id, races, wins, top_fives, top_tens, avg_finish, 
        laps_led_race, fastest_laps_race, avg_pass_diff, quality_passes_race, 
        fppg, practice_laps, practice_best_lap_time, practice_best_lap_speed, 
        qualifying_pos, qualifying_best_lap_time, qualifying_best_lap_speed, 
        laps, miles, surface, restrictor_plate, cautions_race, races_3, 
        finished, wins_3, top_5s, top_10s, avg_place, races_4, finished_4, 
        wins_4, top_5s_4, top_10s_4, avg_place_4, salaryid, owned, hatecount, 
        lovecount, note_pos
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
'''

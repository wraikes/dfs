def get_variables(sport):

    if sport == 'pga':
        pass
        # var_keys = [
        #     'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 'SS',
        #     'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 'HTID',
        #     'OE', 'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 'HTEAM', 'OTEAM',
        #     'Lock', 'Id', 'Events', 'Wins', 'Top 5s', 'Top 10s', 'Avg. Place',
        #     'Cuts Made', 'Cut Made%', 'Vegas Odds', 'Vegas Value', 'Events_1',
        #     'Wins_1', 'Top 5s_1', 'Top 10s_1', 'Avg. Place_1', 'Cuts Made_1', 
        #     'Cut Made%_1',
        #     'Events_2', 'Wins_2', 'Top 5s_2', 'Top 10s_2', 'Avg. Place_2', 
        #     'Cuts Made_2', 'Cut Made%_2', 'GIR%', 'Driving Acc%', 'Driving Dist',
        #     'Putting Avg', 'Scramble%', 'Events_3', 'Avg. Place_3', 'Cuts Made_3',
        #     'Cut Made %', 'GIR%_3', 'Driving Acc%_3', 'Driving Dist_3', 'Putting Avg_3',
        #     'Scramble%_3', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'projections'
        # ]
        
        # var_col_names = 'event_id, s, player_id, name, pos, salary, gid, gi, date, ppg, pp, \
        #     ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, \
        #     htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, \
        #     oteam, lock, id, events, wins, top_5s, top_10s, avg_place, \
        #     cuts_made, cut_made, vegas_odds, vegas_value, events_1, wins_1, \
        #     top_5s_1, top_10s_1, avg_place_1, cuts_made_1, cut_made_1, \
        #     events_2, wins_2, top_5s_2, top_10s_2, avg_place_2, cuts_made_2, \
        #     cut_made_2, gir, driving_acc, driving_dist, putting_avg, scramble, \
        #     events_3, avg_place_3, cuts_made_3, cut_made_3, gir_3, \
        #     driving_acc_3, driving_dist_3, putting_avg_3, scramble_3, salaryid, \
        #     owned, hatecount, lovecount, projections'
        
    elif sport == 'nascar':
        pass
    
    elif sport == 'nba':
        var_keys = [
            'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 
            'SS', 'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 
            'HTID', 'OE', 'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 
            'HTEAM', 'OTEAM', 'Lock', 'Id', 
            'PTS/G_0', 'REB/G_0', 'AST/G_0', 'STL+BLK/G_0', 'Mins/G_0', 
            'Impact Est_0', 'Usage_0', 'FPPM_0', 'FPPG_0', 'Home/Away_0', 'Fav/Dog_0', 
            'PTS/G_1', 'REB/G_1', 'AST/G_1', 'STL+BLK/G_1', 'Mins/G_1', 
            'Impact Est_1', 'Usage_1', 'FPPM_1', 'FPPG_1', 'Home/Away_1', 'Fav/Dog_1', 
            'PTS/G_2', 'REB/G_2', 'AST/G_2', 'STL+BLK/G_2', 'Mins/G_2', 
            'Impact Est_2', 'Usage_2', 'FPPM_2', 'FPPG_2', 'Home/Away_2', 'Fav/Dog_2',
            'PTS/G_3', 'REB/G_3', 'AST/G_3', 'STL+BLK/G_3', 'Mins/G_3', 
            'Impact Est_3', 'Usage_3', 'FPPM_3', 'FPPG_3', 'Home/Away_3', 'Fav/Dog_3',
            'PTS/G_4', 'REB/G_4', 'AST/G_4', 'STL/G_4', 'BLK/G_4', 'Plus-Minus_4', 
            'Overall Rank_4', 'FPPG_4', 'Home/Away_4', 'Fav/Dog_4',
            'PTS/G_5', 'REB/G_5', 'AST/G_5', 'STL/G_5', 'BLK/G_5', 'Plus-Minus_5', 
            'Overall Rank_5', 'FPPG_5', 'Home/Away_5', 'Fav/Dog_5',
            'PTS/G_6', 'REB/G_6', 'AST/G_6', 'STL/G_6', 'BLK/G_6', 'Plus-Minus_6', 
            'Overall Rank_6', 'FPPG_6', 'Home/Away_6', 'Fav/Dog_6',
            'PTS/G_7', 'REB/G_7', 'AST/G_7', 'STL/G_7', 'BLK/G_7', 'Plus-Minus_7', 
            'Overall Rank_7', 'FPPG_7', 'Home/Away_7', 'Fav/Dog_7',        
            'PTS/G_8', 'REB/G_8', 'AST/G_8', 'STL/G_8', 'BLK/G_8', 'Plus-Minus_8', 
            'Overall Rank_8', 'FPPG_8', 'Home/Away_8', 'Fav/Dog_8',
            'PTS/G_9', 'REB/G_9', 'AST/G_9', 'STL/G_9', 'BLK/G_9', 'Plus-Minus_9', 
            'Overall Rank_9', 'FPPG_9', 'Home/Away_9', 'Fav/Dog_9',
            'PTS/G_10', 'REB/G_10', 'AST/G_10', 'STL/G_10', 'BLK/G_10', 'Pace_10', 
            'Pace Diff_10', 'Overall Rank_10', 'FPPG_10', 'Home/Away_10', 
            'Fav/Dog_10', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'projections'
        ]
        
        var_col_names = 'event_id, s, player_id, name, pos, salary, \
            gid, gi, date, ppg, pp, ps, ss, stat, is_, notes, floor, ceil, \
            conf, ptid, otid, htid, oe, opprank, opptotal, dspid, dgid, \
            img, pteam, hteam, oteam, lock, id, pts_g_0, reb_g_0, ast_g_0, \
            stl_blk_g_0, mins_g_0, impact_est_0, usage_0, fppm_0, fppg_0, \
            home_away_0, fav_dog_0, pts_g_1, reb_g_1, ast_g_1, stl_blk_g_1, \
            mins_g_1, impact_est_1, usage_1, fppm_1, fppg_1, home_away_1, \
            fav_dog_1, pts_g_2, reb_g_2, ast_g_2, stl_blk_g_2, mins_g_2, \
            impact_est_2, usage_2, fppm_2, fppg_2, home_away_2, fav_dog_2, \
            pts_g_3, reb_g_3, ast_g_3, stl_blk_g_3, mins_g_3, impact_est_3, \
            usage_3, fppm_3, fppg_3, home_away_3, fav_dog_3, pts_g_4, \
            reb_g_4, ast_g_4, stl_g_4, blk_g_4, plus_minus_4, overall_rank_4, \
            fppg_4, home_away_4, fav_dog_4, pts_g_5, reb_g_5, ast_g_5, \
            stl_g_5, blk_g_5, plus_minus_5, overall_rank_5, fppg_5, home_away_5, \
            fav_dog_5, pts_g_6, reb_g_6, ast_g_6, stl_g_6, blk_g_6, plus_minus_6, \
            overall_rank_6, fppg_6, home_away_6, fav_dog_6, pts_g_7, reb_g_7, \
            ast_g_7, stl_g_7, blk_g_7, plus_minus_7, overall_rank_7, fppg_7, \
            home_away_7, fav_dog_7, pts_g_8, reb_g_8, ast_g_8, stl_g_8, blk_g_8, \
            plus_minus_8, overall_rank_8, fppg_8, home_away_8, fav_dog_8, \
            pts_g_9, reb_g_9, ast_g_9, stl_g_9, blk_g_9, plus_minus_9, \
            overall_rank_9, fppg_9, home_away_9, fav_dog_9, pts_g_10, reb_g_10, \
            ast_g_10, stl_g_10, blk_g_10, pace_10, pace_diff_10, overall_rank_10, \
            fppg_10, home_away_10, fav_dog_10, salary_id, owned, hatecount, \
            lovecount, projections'
    
    elif sport == 'nhl':
        pass
        
    return var_keys, var_col_names


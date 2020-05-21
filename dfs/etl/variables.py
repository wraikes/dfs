def transform_variables(var_keys):
        tmp = [x.lower().replace(' ', '_').replace('/', '_').replace('+', '_').replace('-', '_').replace(':', '_') for x in var_keys]
        tmp = [x.replace('.', '').replace('?', '').replace('%', '') for x in tmp]
        tmp = ['player_id' if x == 'pid' else x for x in tmp]
        tmp = ['date' if x == 'gt' else x for x in tmp]
        tmp = ['is_' if x == 'is' else x for x in tmp]
        
        return ', '.join(tmp)    

def get_variables(sport):

    if sport == 'nascar':
        var_keys = [
            'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 'SS', 
            'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 'HTID', 'OE', 
            'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 'HTEAM', 'OTEAM', 
            'Lock', 'Id', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'Races_0', 
            'Wins_0', 'Top Fives_0', 'Top Tens_0', 'Avg Finish_0', 'Laps Led/Race_0', 
            'Fastest Laps/Race_0', 'Avg Pass Diff_0', 'Quality Passes/Race_0', 'FPPG_0', 
            'Practice Laps_1', 'Practice Best Lap Time_1', 'Practice Best Lap Speed_1', 
            'Qualifying Pos_1', 'Qualifying Best Lap Time_1', 'Qualifying Best Lap Speed_1', 
            'Laps_2', 'Miles_2', 'Surface_2', 'Restrictor Plate?_2', 'Cautions/Race_2', 
            'Races_3', 'Finished_3', 'Wins_3', 'Top 5s_3', 'Top 10s_3', 'Avg. Place_3', 
            'Races_4', 'Finished_4', 'Wins_4', 'Top 5s_4', 'Top 10s_4', 'Avg. Place_4',
            'projections'
        ]
        
    elif sport == 'lol':
        var_keys = [
            'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 'SS', 
            'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 'HTID', 'OE', 
            'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 'HTEAM', 'OTEAM', 
            'Lock', 'Id', 'SalaryId', 'Owned', 'HateCount', 'LoveCount',
            'Best Of_0', 'Odds_0', 'FPPG vs Opp_0', 'MatchPlay%_1'
        
        ]
        

    elif sport == 'pga':
        var_keys = [
            'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 'SS', 
            'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 'HTID', 'OE', 
            'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 'HTEAM', 'OTEAM', 
            'Lock', 'Id', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'Events_0', 
            'Wins_0', 'Top 5s_0', 'Top 10s_0', 'Avg. Place_0', 'Cuts Made_0', 
            'Cut Made%_0', 'Vegas Odds_0', 'Vegas Value_0', 'Events_1', 'Wins_1', 
            'Top 5s_1', 'Top 10s_1', 'Avg. Place_1', 'Cuts Made_1', 'Cut Made%_1',
            'Events_2', 'Wins_2', 'Top 5s_2', 'Top 10s_2', 'Avg. Place_2', 
            'Cuts Made_2', 'Cut Made%_2', 'GIR%_2', 'Driving Acc%_2', 'Driving Dist_2',
            'Putting Avg_2', 'Scramble%_2', 'Events_3', 'Avg. Place_3', 'Cuts Made_3',
            'Cut Made %_3', 'GIR%_3', 'Driving Acc%_3', 'Driving Dist_3', 'Putting Avg_3',
            'Scramble%_3', 'projections' 
        ]
        
        
    # elif sport == 'pga':
    #     var_keys = [
    #         'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 'SS',
    #         'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 'HTID',
    #         'OE', 'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 'HTEAM', 'OTEAM',
    #         'Lock', 'Id', 'Events_0', 'Wins_0', 'Top 5s_0', 'Top 10s_0', 'Avg. Place_0',
    #         'Cuts Made_0', 'Cut Made%_0', 'Vegas Odds_0', 'Vegas Value_0', 'Events_1',
    #         'Wins_1', 'Top 5s_1', 'Top 10s_1', 'Avg. Place_1', 'Cuts Made_1', 
    #         'Cut Made%_1',
    #         'Events_2', 'Wins_2', 'Top 5s_2', 'Top 10s_2', 'Avg. Place_2', 
    #         'Cuts Made_2', 'Cut Made%_2', 'GIR%_2', 'Driving Acc%_2', 'Driving Dist_2',
    #         'Putting Avg_2', 'Scramble%_2', 'Events_3', 'Avg. Place_3', 'Cuts Made_3',
    #         'Cut Made %_3', 'GIR%_3', 'Driving Acc%_3', 'Driving Dist_3', 'Putting Avg_3',
    #         'Scramble%_3', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'projections'
    #     ]
        
    #     var_col_names = 'event_id, s, player_id, name, pos, salary, gid, gi, date, ppg, pp, \
    #         ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, \
    #         htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, \
    #         oteam, lock, id, events_0, wins_0, top_5s_0, top_10s_0, avg_place_0, \
    #         cuts_made_0, cut_made_0, vegas_odds_0, vegas_value_0, events_1, wins_1, \
    #         top_5s_1, top_10s_1, avg_place_1, cuts_made_1, cut_made_1, \
    #         events_2, wins_2, top_5s_2, top_10s_2, avg_place_2, cuts_made_2, \
    #         cut_made_2, gir_2, driving_acc_2, driving_dist_2, putting_avg_2, scramble_2, \
    #         events_3, avg_place_3, cuts_made_3, cut_made_3, gir_3, \
    #         driving_acc_3, driving_dist_3, putting_avg_3, scramble_3, salaryid, \
    #         owned, hatecount, lovecount, projections'
        

    
    # elif sport == 'nba':
    #     var_keys = [
    #         'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GI', 'GT', 'PPG', 'PP', 'PS', 
    #         'SS', 'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 
    #         'HTID', 'OE', 'OppRank', 'OppTotal', 'DSPID', 'DGID', 'IMG', 'PTEAM', 
    #         'HTEAM', 'OTEAM', 'Lock', 'Id', 
    #         'PTS/G_0', 'REB/G_0', 'AST/G_0', 'STL+BLK/G_0', 'Mins/G_0', 
    #         'Impact Est_0', 'Usage_0', 'FPPM_0', 'FPPG_0', 'Home/Away_0', 'Fav/Dog_0', 
    #         'PTS/G_1', 'REB/G_1', 'AST/G_1', 'STL+BLK/G_1', 'Mins/G_1', 
    #         'Impact Est_1', 'Usage_1', 'FPPM_1', 'FPPG_1', 'Home/Away_1', 'Fav/Dog_1', 
    #         'PTS/G_2', 'REB/G_2', 'AST/G_2', 'STL+BLK/G_2', 'Mins/G_2', 
    #         'Impact Est_2', 'Usage_2', 'FPPM_2', 'FPPG_2', 'Home/Away_2', 'Fav/Dog_2',
    #         'PTS/G_3', 'REB/G_3', 'AST/G_3', 'STL+BLK/G_3', 'Mins/G_3', 
    #         'Impact Est_3', 'Usage_3', 'FPPM_3', 'FPPG_3', 'Home/Away_3', 'Fav/Dog_3',
    #         'PTS/G_4', 'REB/G_4', 'AST/G_4', 'STL/G_4', 'BLK/G_4', 'Plus-Minus_4', 
    #         'Overall Rank_4', 'FPPG_4', 'Home/Away_4', 'Fav/Dog_4',
    #         'PTS/G_5', 'REB/G_5', 'AST/G_5', 'STL/G_5', 'BLK/G_5', 'Plus-Minus_5', 
    #         'Overall Rank_5', 'FPPG_5', 'Home/Away_5', 'Fav/Dog_5',
    #         'PTS/G_6', 'REB/G_6', 'AST/G_6', 'STL/G_6', 'BLK/G_6', 'Plus-Minus_6', 
    #         'Overall Rank_6', 'FPPG_6', 'Home/Away_6', 'Fav/Dog_6',
    #         'PTS/G_7', 'REB/G_7', 'AST/G_7', 'STL/G_7', 'BLK/G_7', 'Plus-Minus_7', 
    #         'Overall Rank_7', 'FPPG_7', 'Home/Away_7', 'Fav/Dog_7',        
    #         'PTS/G_8', 'REB/G_8', 'AST/G_8', 'STL/G_8', 'BLK/G_8', 'Plus-Minus_8', 
    #         'Overall Rank_8', 'FPPG_8', 'Home/Away_8', 'Fav/Dog_8',
    #         'PTS/G_9', 'REB/G_9', 'AST/G_9', 'STL/G_9', 'BLK/G_9', 'Plus-Minus_9', 
    #         'Overall Rank_9', 'FPPG_9', 'Home/Away_9', 'Fav/Dog_9',
    #         'PTS/G_10', 'REB/G_10', 'AST/G_10', 'STL/G_10', 'BLK/G_10', 'Pace_10', 
    #         'Pace Diff_10', 'Overall Rank_10', 'FPPG_10', 'Home/Away_10', 
    #         'Fav/Dog_10', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'projections'
    #     ]
        
    #     var_col_names = 'event_id, s, player_id, name, pos, salary, \
    #         gid, gi, date, ppg, pp, ps, ss, stat, is_, notes, floor, ceil, \
    #         conf, ptid, otid, htid, oe, opprank, opptotal, dspid, dgid, \
    #         img, pteam, hteam, oteam, lock, id, pts_g_0, reb_g_0, ast_g_0, \
    #         stl_blk_g_0, mins_g_0, impact_est_0, usage_0, fppm_0, fppg_0, \
    #         home_away_0, fav_dog_0, pts_g_1, reb_g_1, ast_g_1, stl_blk_g_1, \
    #         mins_g_1, impact_est_1, usage_1, fppm_1, fppg_1, home_away_1, \
    #         fav_dog_1, pts_g_2, reb_g_2, ast_g_2, stl_blk_g_2, mins_g_2, \
    #         impact_est_2, usage_2, fppm_2, fppg_2, home_away_2, fav_dog_2, \
    #         pts_g_3, reb_g_3, ast_g_3, stl_blk_g_3, mins_g_3, impact_est_3, \
    #         usage_3, fppm_3, fppg_3, home_away_3, fav_dog_3, pts_g_4, \
    #         reb_g_4, ast_g_4, stl_g_4, blk_g_4, plus_minus_4, overall_rank_4, \
    #         fppg_4, home_away_4, fav_dog_4, pts_g_5, reb_g_5, ast_g_5, \
    #         stl_g_5, blk_g_5, plus_minus_5, overall_rank_5, fppg_5, home_away_5, \
    #         fav_dog_5, pts_g_6, reb_g_6, ast_g_6, stl_g_6, blk_g_6, plus_minus_6, \
    #         overall_rank_6, fppg_6, home_away_6, fav_dog_6, pts_g_7, reb_g_7, \
    #         ast_g_7, stl_g_7, blk_g_7, plus_minus_7, overall_rank_7, fppg_7, \
    #         home_away_7, fav_dog_7, pts_g_8, reb_g_8, ast_g_8, stl_g_8, blk_g_8, \
    #         plus_minus_8, overall_rank_8, fppg_8, home_away_8, fav_dog_8, \
    #         pts_g_9, reb_g_9, ast_g_9, stl_g_9, blk_g_9, plus_minus_9, \
    #         overall_rank_9, fppg_9, home_away_9, fav_dog_9, pts_g_10, reb_g_10, \
    #         ast_g_10, stl_g_10, blk_g_10, pace_10, pace_diff_10, overall_rank_10, \
    #         fppg_10, home_away_10, fav_dog_10, salary_id, owned, hatecount, \
    #         lovecount, projections'
    
    var_col_names = transform_variables(var_keys)

    return var_keys, var_col_names


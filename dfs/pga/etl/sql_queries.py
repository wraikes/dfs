query_insert_sportsline_pro = '''
    INSERT INTO {}_sportsline_pro (
        link_pro, title_pro, date_pro, name, dfs_pick_dk 
    ) VALUES (
        %s, %s, %s, %s, %s
    )
'''

query_insert_sportsline_betting = '''
    INSERT INTO {}_sportsline_betting (
        link_betting, title_betting, date_betting, name, 
        pos_betting, pos_odds_betting
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
'''

query_insert_sportsline_leaderboard = '''
    INSERT INTO {}_sportsline_picks (
        link_lead, title_lead, date_lead, name,
        pos_lead
    ) VALUES (
        %s, %s, %s, %s, %s
    )
'''

query_insert_linestarapp = '''
    INSERT INTO {}_linestarapp_{} (
    {}
    ) VALUES (
    {}
    )
'''

# pga_linestarapp_insert = '''
#     INSERT INTO pga_linestarapp_{} (
#     {}
#         event_id, s, player_id, name, pos, salary, gid, gi, pga_date, 
#         ppg, pp, ps, ss, stat, is_, notes, floor, ceil, conf, ptid, otid, 
#         htid, oe, opprank, opptotal, dspid, dgid, img, pteam, hteam, oteam, 
#         lock, id, events, wins, top_5s, top_10s, avg_place, cuts_made,
#         cut_made, vegas_odds, vegas_value, events_1, wins_1, top_5s_1,
#         top_10s_1, avg_place_1, cuts_made_1, cut_made_1, events_2, wins_2,
#         top_5s_2, top_10s_2, avg_place_2, cuts_made_2, cut_made_2, gir,
#         driving_acc, driving_dist, putting_avg, scramble, events_3, 
#         avg_place_3, cuts_made_3, cut_made_3, gir_3, driving_acc_3, 
#         driving_dist_3, putting_avg_3, scramble_3, salaryid, owned, hatecount,
#         lovecount
#     ) VALUES (
#     {}
#         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
#     )
# '''
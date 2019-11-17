def get_raw_vars(sport):

    if sport == 'pga':
        vars = [
            'S', 'PID', 'Name', 'POS', 'SAL', 'GID', 'GT', 'PPG', 'PP', 'PS', 'SS',
            'STAT', 'IS', 'Notes', 'Floor', 'Ceil', 'Conf', 'PTID', 'OTID', 'HTID',
            'OE', 'OppRank', 'DSPID', 'DGID', 'IMG', 'PTEAM', 'HTEAM', 'OTEAM',
            'Lock', 'Id', 'Events', 'Wins', 'Top 5s', 'Top 10s', 'Avg. Place',
            'Cuts Made', 'Cut Made%', 'Vegas Odds', 'Vegas Value', 'Events_1',
            'Wins_1', 'Top 5s_1', 'Top 10s_1', 'Avg. Place_1', 'Cut Made%_1',
            'Events_2', 'Wins_2', 'Top 5s_2', 'Top 10s_2', 'Avg. Place_2', 
            'Cuts Made_2', 'Cut Made%_2', 'GIR%', 'Driving Acc%', 'Driving Dist',
            'Putting Avg', 'Scramble%', 'Events_3', 'Avg. Place_3', 'Cuts Made_3',
            'Cut Made %', 'GIR%_3', 'Driving Acc%_3', 'Driving Dist_3', 'Putting Avg_3',
            'Scramble%_3', 'SalaryId', 'Owned', 'HateCount', 'LoveCount', 'projections'
        ]
        
    return vars

# #this could be replaced with appropriate lower() & special character removal
# pga_clean = [
#     x.replace(' ', '_').replace('%', '').lower() for x in pga_raw
# ]


# [
#     's', 'player_id', 'name', 'pos', 'salary', 'gid', 'gi', 'date', 'ppg', 'pp',
#     'ps', 'ss', 'stat', 'is_', 'notes', 'floor', 'ceil', 'conf', 'ptid', 'otid', 
#     'htid', 'oe', 'opprank', 'opptotal', 'dspid', 'dgid', 'img', 'pteam', 'hteam', 
#     'oteam', 'lock', 'id', 'events', 'wins', 'top_5s', 'top_10s', 'avg_place',
#     'cuts_made', 'cut_made', 'vegas_odds', 'vegas_value', 'events_1', 'wins_1',
#     'top_5s_1', 'top_10s_1', 'avg_place_1', 'cuts_made_1', 'cut_made_1',
#     'events_2', 'wins_2', 'top_5s_2', 'top_10s_2', 'avg_place_2', 'cuts_made_2',
#     'cut_made_2', 'gir', 'driving_acc', 'driving_dist', 'putting_avg', 'scramble',
#     'events_3', 'avg_place_3', 'cuts_made_3', 'cut_made_3', 'gir_3', 
#     'driving_acc_3', 'driving_dist_3', 'putting_avg_3', 'scramble_3', 'salaryid',
#     'owned', 'hatecount', 'lovecount' 
# ]
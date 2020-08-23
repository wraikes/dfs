query_delete_projections = '''
    DELETE FROM {}_linestarapp_{} WHERE projections = 'true'
'''


query_insert_sportsline_pro = '''
    INSERT INTO {}_sportsline_pro (
        link_pro, title_pro, date_pro, name, dfs_pick_dk 
    ) VALUES (
        %s, %s, %s, %s, %s
    )
'''

query_insert_sportsline_bet = '''
    INSERT INTO {}_sportsline_bet (
        link_bet, title_bet, date_bet, name, 
        pos_bet, pos_odds_bet
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
'''

query_insert_sportsline_lead = '''
    INSERT INTO {}_sportsline_lead (
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

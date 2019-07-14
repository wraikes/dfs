import json
import requests


def site_load(pid=209):
    html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport=9&site=2&periodId={}'.format(pid)
    page = requests.get(html).content.decode()   
    json_data = json.loads(page)

    match_data = matchup_data(json_data)
    owner_data = ownership_data(json_data)
    final_data = combine_data(owner_data, match_data)
    

def matchup_data(data):
    table_values = dict()
        
    for i in range(len(data['MatchupData'])):
        columns = data['MatchupData'][i]['Columns']
        
        for player in range(len(data['MatchupData'][i]['PlayerMatchups'])):
            tmp_data = data['MatchupData'][i]['PlayerMatchups'][player]
            p_id = tmp_data['PlayerId']
            values = dict(zip(columns, tmp_data['Values']))
            
            if p_id not in table_values.keys():
                table_values[p_id] = values
            else:
                for key, value in values.items():
                    table_values[p_id][key] = value
                    
    return table_values


def ownership_data(data):
    ownership_values = []
        
    for player in range(len(data['Ownership']['Salaries'])):
        ownership_values.append(data['Ownership']['Salaries'][player])
        
    return ownership_values


def combine_data(owner_data, table_data):
    for i in range(len(owner_data)):
        player_id = owner_data[i]['PID']
            
        for key, value in table_data[player_id].items():
            owner_data[i][key] = value
            
    return owner_data


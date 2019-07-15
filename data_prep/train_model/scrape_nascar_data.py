'''Pull FanDuel historical data & projections. Note pid starts at 209.
'''
import json
import requests


class NascarDataPull:

    def __init__(self, train=True, prediction=False, pid=257):
        self.train = train
        self.prediction = prediction
        self.pid = pid
        
        self._start_pid = 209 if self.train else self.pid
        self._json_data = []
        self._final_data = {}
    
    
    def pull_json_data(self):

        for pid in range(self._start_pid, self.pid+1):
            html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport=9&site=2&periodId={}'.format(pid)
            page = requests.get(html).content.decode() 
            data = json.loads(page)
            self._json_data.append(data)
    
    
    def extract_owner_data(self):
        
        for race in self._json_data:
            race_id = race['Ownership']['PeriodId']
            self._final_data[race_id] = {}
            
            for player_data in race['Ownership']['Salaries']:
                player_id = player_data['PID']
                self._final_data[race_id][player_id] = player_data
    
    
    def extract_table_data(self):
        for race in self._json_data:
            race_id = race['Ownership']['PeriodId']
            
            for i, table in enumerate(race['MatchupData']):
                col_names = table['Columns']
                id_store = []
            
                for player in table['PlayerMatchups']:
                    player_id = player['PlayerId']
    
                    if player_id in id_store or player_id not in self._final_data[race_id].keys():
                        continue
                    else:
                        id_store.append(player_id)
                        
                    player_dict = dict(zip(col_names, player['Values']))                 
                    
                    for key, value in player_dict.items():
                        if key in self._final_data[race_id][player_id].keys():
                            self._final_data[race_id][player_id]['{}_{}'.format(key, i)] = value                 
    
                        else:
                            self._final_data[race_id][player_id][key] = value
                            
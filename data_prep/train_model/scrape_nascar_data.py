import json
import requests


class DataPull:
    '''
    pid starts at 209
    '''
    
    def __init__(self, train, prediction, pid):
        self.train = train
        self.prediction = prediction
        self.pid = pid
        
        self._start_pid = 209 if self.train else self.pid
        self._json_data = []
        self._table_data = []
        self._owner_data = []
        self._final_data = []
    
    def pull_json_data(self):

        for pid in range(self._start_pid, self.pid+1):
            html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport=9&site=2&periodId={}'.format(pid)
            page = requests.get(html).content.decode()   
            self._json_data.append(json.loads(page))   
    
    
    def extract_matchupdata(self):
        
        for race in self._json_data:
            tables = dict()

            for i, table in enumerate(race['MatchupData']):
                col_names = table['Columns']
                id_store = []
            
                for player in table['PlayerMatchups']:
                    player_id = player['PlayerId']

                    if player_id in id_store:
                        continue
                    else:
                        id_store.append(player_id)
                        
                    player_dict = dict(zip(col_names, player['Values']))                    
                    
                    if player_id not in tables.keys():
                        tables[player_id] = player_dict
                        
                    else:
                        for key, value in player_dict.items():
                            if key in tables[player_id].keys():
                                tables[player_id]['{}_{}'.format(key, i)]= value
                                
                            else:
                                tables[player_id][key] = value
                                
            self._table_data.append(tables)
    
    
    def extract_owner_data(self):
        
        for race in self._json_data:
            owner_data = []
                
            for player_data in data['Ownership']['Salaries']:
                owner_data.append(player_data)
                
            self._owner_data.append(owner_data)
        
        
    def final_data(self):
        for i in owner_data:
            player_id = owner_data[i]['PID']
                    
            for key, value in table_data[player_id].items():
                owner_data[i][key] = value
                    
        return owner_data




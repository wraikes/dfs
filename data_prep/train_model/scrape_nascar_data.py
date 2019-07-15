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
        
        self._json_data = []
        self._table_data = []
        self._owner_data = []
        self._final_data = []
    
    def pull_json_data(self):
        if self.train:
            _start_pid = 209
        else:
            _start_pid = self.pid
            
        for _pid in range(_start_pid, self.pid+1):
            _html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport=9&site=2&periodId={}'.format(_pid)
            _page = requests.get(_html).content.decode()   
            self._json_data.append(json.loads(_page))   
    
    
    def extract_matchupdata(self):
        
        for _json in self._json_data:
            _table_values = dict()

            for i in range(len(data['MatchupData'])):
                col_names = data['MatchupData'][i]['Columns']
            
                for player_data in data['MatchupData'][i]['PlayerMatchups']:
                    player_id = player_data['PlayerId']
                    player_dict = dict(zip(col_names, player_data['Values']))
                    
                    if player_id not in _table_values.keys():
                        _table_values[player_id] = player_dict
                    else:
                        for key, value in player_dict.items():
                            if _table_values[player_id][key]:
                                table_values[player_id]['{}_{}'.format(key, i] = value
                            else:
                                _table_values[player_id][key] = value
                                
            self._table_data.append(_table_values)
    
    
    def extract_owner_data(self):
        
        for _data in self._json_data:
            owner_values = []
                
            for player_data in data['Ownership']['Salaries']:
                owner_values.append(player_data)
                
            self._owner_data.append(owner_values)
        
        
    def final_data(self):
        for i in owner_data:
            player_id = owner_data[i]['PID']
                    
            for key, value in table_data[player_id].items():
                owner_data[i][key] = value
                    
        return owner_data




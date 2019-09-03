import json
import requests

class DataPull:
    
    parameters = {
        'nascar': {{
            'sport': 9,
            'pid_start': 209
        },
        'pga': {{
            'sport': 5,
            'pid_start': 112
        },
        'nhl': {{
            'sport': 6,
            'pid_start': 338
        },
        'nba': {{
            'sport': 2,
            'pid_start': 304
        },
        'nfl': {{
            'sport': 1,
            'pid_start': 81
        }

        'mlb': {{
            'sport': 3,
            'pid_start': 550
        }
    }
    
    def __init__(self, sport, pid_end):
        self.sport = parameters[sport]['sport']
        self.pid_star = parameters[sport]['pid_start']
        
        self.pid_end = pid_end
        self.html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport={}&site=2&periodId='.format(self.sport)
        

    def pull_json_data(self):

        for pid in range(self.start_pid, self.pid_end + 1):
            html = self.html + str(pid)
            page = requests.get(html).content.decode() 
            data = json.loads(page)
            #save to appropriate dynamodb
    
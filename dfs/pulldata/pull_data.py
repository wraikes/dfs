import json
import requests
import boto3

class LinestarappData:
    
    s3 = boto3.resource('s3')
    parameters = {
        'nascar': {
            'sport': 9,
            'pid_start': 209
        },
        'pga': {
            'sport': 5,
            'pid_start': 112
        },
        'nhl': {
            'sport': 6,
            'pid_start': 338
        },
        'nba': {
            'sport': 2,
            'pid_start': 304
        },
        'nfl': {
            'sport': 1,
            'pid_start': 81
        },
        'mlb': {
            'sport': 3,
            'pid_start': 550
        }
    }
    
    
    def __init__(self, sport):
        self.sport = sport
        self.sport_id = self.parameters[sport]['sport']
        self.pid_start = self.parameters[sport]['pid_start']

        self.html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport={}&site=2&periodId='.format(self.sport_id)
        self.bucket = 'my-dfs-data'
        self.folder = '{}/linestarapp'.format(sport)


    def pull_historical_data(self, pid_end):

        for pid in range(self.pid_start, pid_end + 1):
            html = self.html + str(pid)
            page = requests.get(html).content.decode() 
            data = json.loads(page)
            
            obj = self.s3.Object(self.bucket, '{}/{}.json'.format(self.folder, pid))
            obj.put(
                Body=(json.dumps(data))
            )

            print(pid)


    def update_data(self, projections=False):
        # look at most recent pull pid
        # loop thru pid's and pull until reach stopped point based on what was pulled
            # save to appropriate s3
        bucket = self.s3.Bucket(self.bucket)
            
        max_pid = 0
        for obj in bucket.objects.all():
            if self.sport in obj.key and 'json' in obj.key:
                pid = int(obj.key.split('/')[-1].split('.')[0])
                if pid > max_pid:
                    max_pid = pid
        
        if projections:
            max_pid -= 1
            
        while True:
            max_pid += 1
            html = self.html + str(max_pid)
            page = requests.get(html).content.decode() 
            if len(page) < 1000:
                break
            
            data = json.loads(page)
            obj = self.s3.Object(self.bucket, '{}/{}.json'.format(self.folder, max_pid))
            obj.put(
                Body=(json.dumps(data))
            )

            print(max_pid)    


class FantasyNerd:
    pass


class SportsLine:
    pass




if __name__ == '__main__':
    sports = {
        'nascar': 263,
        'nfl': 133,
        'mlb': 1310,
        'nba': 1033,
        'nhl': 1121,
        'pga': 222
    }
    
    for key, value in sports.items():
        print(key)
        data = LinestarappData(key, value)
        data.pull_json_data()

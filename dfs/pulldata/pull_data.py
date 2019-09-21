import json
import requests
import boto3

class LinestarappData:
    
    s3 = boto3.resource('s3')
    bucket = 'my-dfs-data'
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
    
    s3 = boto3.resource('s3')
    bucket = 'my-dfs-data'

    login = 'https://secure.sportsline.com/login'
    payload = {
        'dummy::login_form': '1',
        'form::login_form': 'login_form',
        'xurl': 'http://secure.sportsline.com/',
        'master_product': '23350',
        'vendor': 'sportsline',
        'form_location': 'log_in_page',
        'userid': '*', 
        'password': '*'
    }
    
    
    def __init__(self, sport):
        self.sport = sport #confined to nhl, nascar, nfl, golf, nba, mlb
        self.articles = 'https://www.sportsline.com/sportsline-web/service/v1/articleIndexContent?slug={}&limit=10000&auth=1'.format(self.sport)
        self.url = 'https://www.sportsline.com/sportsline-web/service/v1/articles/{}?auth=1'
        self.folder = '{}/sportsline'.format(sport)
    
    
    def _get_links(self):
        page = json.loads(requests.get(self.articles).content.decode())
        links = []
        
        for article in page['articles']:
            art = article['slug']
            
            #nascar specific, need to modify for other sports
            if art.endswith('from-a-dfs-pro') or art.startswith('nascar-at') or art.startswith('projected-nascar-leaderboard'):
                links.append(article['slug'])
            
        return links

        
    def articles_to_s3(self):

        links = self._get_links()
        #TO DO: check to see which links are not in s3
        
        with requests.Session() as session:
            post = session.post(self.login, data=self.payload)
            
            for link in links:
                article = self.url.format(link)
                page = session.get(article)
            
                obj = self.s3.Object(self.bucket, '{}/{}'.format(self.folder, link))
                obj.put(
                    Body=(page.text)
                )
    
                print(link)  
    

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

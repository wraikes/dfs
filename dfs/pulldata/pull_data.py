#todo: Nascar specific, need to scale to other sports 
    #mark 'projections' for relevant s3 objects in diff sport
    #find relevant phrasing for sportsline articles in diff sport 

import json
import requests
import boto3
import config

cfg = configparser.ConfigParser()
cfg.read('pull_data.config')
user_id = cfg['SPORTSLINE']['user_id']
password = cfg['SPORTSLINE']['password']

class LinestarappData:
    '''Class to download Linestarapp Data into S3.
    
    Parameters:
        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
        site: 'fd' or 'dk'
    
    Attributes:
        
    '''
    s3 = boto3.resource('s3')
    bucket_name = 'my-dfs-data'
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
    

    def __init__(self, sport, site='fd'):
        '''Initialize class'''
        self.sport = sport
        self.site = site
        
        self.site_id = 2 if site == 'fd' else 1
        self.sport_id = self.parameters[self.sport]['sport']
        self.pid_start = self.parameters[self.sport]['pid_start']

        self.html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport={}&site={}&periodId='.format(self.sport_id, self.site_id)
        self.folder = '{}/linestarapp/'.format(self.sport)

    def _pull_json_data(self, pid):
        '''Internal method for pulling json data from html page'''
        html = self.html + str(pid)
        page = requests.get(html).content.decode() 
        data = json.loads(page)       

        return data


    def update_data(self):
        '''Update missing json data, or update projection data to full data'''
        bucket = self.s3.Bucket(self.bucket_name)
        max_pid = self.pid_start
        
        for obj in bucket.objects.all():
            if self.sport in obj.key and 'json' in obj.key:
                
                #update projections only data
                if 'projections' in obj.key:

                    pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
                    data = _pull_json_data(pid)
                  
                    if max_pid < pid:
                        max_pid = pid
                    
                    #check to see if projections were uploaded
                    sum_pts = sum([x['PS'] for x in data['Ownership']['Salaries']])
                    if sum_pts == 0:
                        continue

                    #save new complete data
                    new_obj = self.s3.Object(
                        self.bucket_name,
                        '{}/{}_{}.json'.format(self.folder, self.site, max_pid)
                    )
                    new_obj.put(
                        Body=(json.dumps(data))
                    )    
                    
                    #delete old projections data
                    self.s3.Object('my-dfs-data', obj.key).delete()
                
                #if not projections data, update max pid to record gaps
                else:
                    pid = int(obj.key.split('/')[-1].split('.')[0].split('_')[1])
                
                    if max_pid < pid:
                        max_pid = pid
        
        #create s3 objects for any missing linestarapp data
        while True:
            data = _pull_json_data(pid)
            
            sum_pts = sum([x['PS'] for x in data['Ownership']['Salaries']])
            if sum_pts != 0:
                object_name = '{}/{}_{}.json'.format(self.folder, self.site, pid)
            else:
                object_name = '{}/{}_{}_projections.json'.format(self.folder, self.site, pid)
            
            #if data is short, it indicates no new data
            if len(str(data)) < 10000:
                break
            
            #save new complete data
            obj = self.s3.Object(self.bucket, '{}/{}_{}.json'.format(self.folder, self.site, max_pid))
            obj.put(
                Body=(json.dumps(data))
            )

            max_pid += 1
            print(max_pid)    


class FantasyNerd:
    pass


class SportsLine:
    '''Class to download Sportsline articles into S3.
    
    Parameters:
        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
        
    '''
    s3 = boto3.resource('s3')
    bucket_name = 'my-dfs-data'

    login = 'https://secure.sportsline.com/login'
    payload = {
        'dummy::login_form': '1',
        'form::login_form': 'login_form',
        'xurl': 'http://secure.sportsline.com/',
        'master_product': '23350',
        'vendor': 'sportsline',
        'form_location': 'log_in_page',
        'userid': user_id,
        'password': password
    }
    
    
    def __init__(self, sport):
        self.sport = sport #confined to nhl, nascar, nfl, golf, nba, mlb
        self.articles = 'https://www.sportsline.com/sportsline-web/service/v1/articleIndexContent?slug={}&limit=10000&auth=1'.format(self.sport)
        self.url = 'https://www.sportsline.com/sportsline-web/service/v1/articles/{}?auth=1'
        self.folder = '{}/sportsline'.format(sport)
    
    
    def _get_links(self):
        '''Get relevant article links to download.'''
        page = json.loads(requests.get(self.articles).content.decode())
        links = []
        
        for article in page['articles']:
            art = article['slug']
            
            #nascar specific, need to modify for other sports
            if art.endswith('from-a-dfs-pro') or art.startswith('nascar-at') or art.startswith('projected-nascar-leaderboard'):
                links.append(article['slug'])
            
        return links

        
    def historical_articles_pull(self):
        '''Pull articles and save to s3 bucket'''
        links = self._get_links()
            
        #Open session and post the user_id and password
        with requests.Session() as session:
            post = session.post(self.login, data=self.payload)
            
            for link in links:
                article = self.url.format(link)
                page = session.get(article)
            
                #load article into s3 object.
                obj = self.s3.Object(self.bucket_name, '{}/{}'.format(self.folder, link))
                obj.put(
                    Body=(page.text)
                )
    
                print(link)  
    
    
    def update_articles(self):

        links = self._get_links()
        bucket = self.s3.Bucket(self.bucket_name)

        for obj in bucket.objects.all():
            if 'sportsline' in obj.key and self.sport in obj.key:
                key = obj.key.split('/')[-1]
                if key in links:
                    links.remove(key)
                    
        #Open session and post the user_id and password
        with requests.Session() as session:
            post = session.post(self.login, data=self.payload)

            #open links
            for link in links:
                article = self.url.format(link)
                page = session.get(article)
            
                #save article into s3 object
                obj = self.s3.Object(self.bucket_name, '{}/{}'.format(self.folder, link))
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
        data = LinestarappData(key, site='fd')
        data.pull_historical_data(value)

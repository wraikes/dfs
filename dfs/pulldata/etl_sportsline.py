#todo: Nascar specific, need to scale to other sports 
    #mark 'projections' for relevant s3 objects in diff sport
    #find relevant phrasing for sportsline articles in diff sport 

import json
import requests
import boto3
import configparser

# cfg = configparser.ConfigParser()
# cfg.read('pull_data.config')
# user_id = cfg['SPORTSLINE']['user_id']
# password = cfg['SPORTSLINE']['password']


class SportslineData:
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


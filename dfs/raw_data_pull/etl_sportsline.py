import json
import requests
import boto3
import configparser


class SportslineData:
    '''Class to download Sportsline articles into S3.
    
    Parameters:
        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
        
    '''
    #load s3 bucket details
    s3 = boto3.resource('s3')
    bucket_name = 'my-dfs-data'
    bucket = s3.Bucket(bucket_name)

    #load config parameters for sportsline
    cfg = configparser.ConfigParser()
    cfg.read('./raw_data_pull/etl_sportsline.ini')
    user_id = cfg['SPORTSLINE']['user_id']
    password = cfg['SPORTSLINE']['password']

    #load login details for sportsline
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
        self.sport = sport if sport != 'pga' else 'golf' #confined to nhl, nascar, nfl, pga, nba, mlb
        self.articles = 'https://www.sportsline.com/sportsline-web/service/v1/articleIndexContent?slug={}&limit=10000&auth=1'.format(self.sport)
        self.url = 'https://www.sportsline.com/sportsline-web/service/v1/articles/{}?auth=1'
        self.folder = '{}/sportsline'.format(sport)
    
    
    def _get_links(self):
        '''Get relevant article links to download.'''
        page = json.loads(requests.get(self.articles).content.decode())
        links = []
        
        for article in page['articles']:
            title = article['slug']
            
            if self.sport == 'nascar':
                if title.endswith('from-a-dfs-pro') or title.startswith('nascar-at') or title.startswith('projected-nascar-leaderboard'):
                    links.append(article['slug'])

            elif self.sport == 'golf':
                if title.endswith('from-a-dfs-pro') or title.endswith('has-surprising-picks-and-predictions'):
                    links.append(article['slug'])
                    
        return links
    
    
    def update_articles(self):

        links = self._get_links()
        bucket = self.s3.Bucket(self.bucket_name)

        for obj in bucket.objects.all():
            if self.sport != 'golf':
                if 'sportsline' in obj.key and self.sport in obj.key:
                    key = obj.key.split('/')[-1]
                    if key in links:
                        links.remove(key)
            else:
                if 'sportsline' in obj.key and 'pga' in obj.key:
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
                page = json.loads(page.text)

                #save article into s3 object
                obj = self.s3.Object(self.bucket_name, '{}/{}'.format(self.folder, link))
                obj.put(
                    Body=json.dumps(page['article'])
                )
    
                print(link) 

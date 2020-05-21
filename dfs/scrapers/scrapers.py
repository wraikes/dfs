import json
import requests
import boto3
import configparser
import logging
from datetime import datetime, date

class LinestarappData:
    '''Downloads data from linestarapp site into designated S3 bucket.
    
    Parameters:
        sport: specify 'nascar', 'nfl', 'nba', 'mlb', 'nhl', 'pga' or 'lol'
        site: specify 'fd' (fanduel) or 'dk' (draftkings)
    
    Attributes:
        sport: store sport
        site: store site
        
        
    '''
    # internals for webscraping and data storage
    _s3 = boto3.resource('s3')
    _bucket = _s3.Bucket('my-dfs-data')
    _html_parameters = {
        'nfl': {
            'sport': 1,
            'pid_start': 81
        },
        'nba': {
            'sport': 2,
            'pid_start': 304
        },
        'mlb': {
            'sport': 3,
            'pid_start': 550
        },
        'pga': {
            'sport': 5,
            'pid_start': 112
        },
        'nhl': {
            'sport': 6,
            'pid_start': 338
        },
        'nascar': {
            'sport': 9,
            'pid_start': 209
        },
        'lol': {
            'sport': 13,
            'pid_start': 135
        }
    }
    
    # #load config parameters for linestarapp
    # cfg = configparser.ConfigParser()
    # cfg.read('./raw_data_pull/scraper.ini')
    # user_id = cfg['CREDENTIALS']['user_id']
    # password = cfg['CREDENTIALS']['password']

    # #load login details for linestarapp
    # login = 'https://www.linestarapp.com/login'
    # payload = {
    #     'StylesheetManager_TSSM': '1',
    #     'ScriptManager_TSM': 'login_form',
    #     'xurl': 'https://www.linestarapp.com/login',
    #     'master_product': '23350',
    #     'vendor': 'sportsline',
    #     'form_location': 'log_in_page',
    #     'userid': user_id,
    #     'password': password
    # }
    
    
    def __init__(self, sport, site='fd'):
        self.sport = sport
        self.site = site
        
        _site_id = 2 if site == 'fd' else 1
        _sport_id = self._html_parameters[self.sport]['sport']
        
        self._pid_start = self._html_parameters[self.sport]['pid_start']
        self._html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport={}&site={}&periodId='.format(_sport_id, _site_id)
        self._folder = '{}/linestarapp'.format(self.sport) 
        self._current_date = date.today()
        self._current_time = datetime.now()

        # file for logging records
        logging.basicConfig(
            filename='./logs/{}_linestarapp_raw_data_pull.log'.format(sport), 
            level='INFO',
            filemode='w'
        )
    
    def update_data(self):
        '''Delete projections, then pull and store all relevant json data'''
        self._delete_projections()
        pid = self._get_max_pid() + 1
        
        while True:
            data = self._pull_json_data(pid)

            #if data is empty and date is from prior date, continue, else break loop
            if data['Ownership'] is None:
                logging.shutdown()
                break
            
            elif len(data['Ownership']['Salaries']) == 0:
                _date_str = json.loads(data['SalaryContainerJson'])['Period']['Name']
                _date = datetime.strptime(_date_str, '%b %d, %Y').date()

                if _date < self._current_date:
                    
                    # log pid if empty and not projections
                    logging.error('Date: {}; Time: {}, PID: {}, Status: FAIL.'.format(
                        self._current_date.strftime('%m/%d/%Y'), 
                        self._current_time.strftime('%H:%M:S'),
                        pid)
                    )
                    continue
                
                else:
                    logging.shutdown()
                    break

            # check if projections data and name as such            
            proj = '_projections' if self._check_projection(data) else ''
            object_name = '{}/{}_{}{}.json'.format(self._folder, self.site, pid, proj)
            
            # save new data to s3 bucket
            obj = self._s3.Object(self._bucket.name, object_name)
            obj.put(
                Body=json.dumps(data)
            )

            # log pid and print to console for monitoring
            logging.info('Date: {}; Time: {}, PID: {}, Status: SUCCESS.'.format(
                self._current_date.strftime('%m/%d/%Y'), 
                self._current_time.strftime('%H:%M:S'),
                pid)
            )
            print(self.site, pid)                 
            pid += 1
            
            
    def _delete_projections(self):
        '''If s3 object is a projection, delete object'''
        for obj in self._bucket.objects.all():
            if self.sport in obj.key and 'json' in obj.key and 'projections' in obj.key and self.site in obj.key:
        
                # delete old projections data
                self._s3.Object('my-dfs-data', obj.key).delete()
        
        
    def _get_max_pid(self):
        '''Get maximum pid from sport by looping thru all objects and recording highest pid'''
        max_pid = self._pid_start
        
        for obj in self._bucket.objects.all():
            if self.sport in obj.key and 'json' in obj.key and self.site in obj.key:
                pid = self._get_pid(obj.key)
                
                if max_pid < pid:
                    max_pid = pid

        return max_pid
        

    def _pull_json_data(self, pid):
        '''Pull json data from html page'''
        html = self._html + str(pid)
        page = requests.get(html).content.decode() 
        data = json.loads(page)       

        return data


    def _check_projection(self, data):
        '''Check if json data is projections (True) or historical (False)
        by checking to see if data is from today or has no points scored.'''
        sum_pts = sum([x['PS'] for x in data['Ownership']['Salaries']])
        pid_str_date = data['Ownership']['Salaries'][0]['GT'].split('T')[0]
        pid_date = datetime.strptime(pid_str_date, '%Y-%m-%d').date()

        return sum_pts == 0 or self._current_date == pid_date


    def _get_pid(self, key):
        '''Get pid from object key'''
        pid = int(key.split('/')[-1].split('.')[0].split('_')[1])

        return pid


class FantasyNerdData:
    pass




class SportslineData:
    '''Class to download Sportsline articles into S3.
    
    Parameters:
        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
        
    '''
    pass
    #load s3 bucket details
    # s3 = boto3.resource('s3')
    # bucket_name = 'my-dfs-data'
    # bucket = s3.Bucket(bucket_name)

    # #load config parameters for sportsline
    # cfg = configparser.ConfigParser()
    # cfg.read('./raw_data_pull/etl.ini')
    # user_id = cfg['CREDENTIALS']['user_id']
    # password = cfg['CREDENTIALS']['password']

    # #load login details for sportsline
    # login = 'https://secure.sportsline.com/login'
    # payload = {
    #     'dummy::login_form': '1',
    #     'form::login_form': 'login_form',
    #     'xurl': 'http://secure.sportsline.com/',
    #     'master_product': '23350',
    #     'vendor': 'sportsline',
    #     'form_location': 'log_in_page',
    #     'userid': user_id,
    #     'password': password
    # }
    
    
    # def __init__(self, sport):
    #     self.sport = sport if sport != 'pga' else 'golf' #confined to nhl, nascar, nfl, pga, nba, mlb
    #     self.articles = 'https://www.sportsline.com/sportsline-web/service/v1/articleIndexContent?slug={}&limit=10000&auth=1'.format(self.sport)
    #     self.url = 'https://www.sportsline.com/sportsline-web/service/v1/articles/{}?auth=1'
    #     self.folder = '{}/sportsline'.format(sport)
    
    
    # def _get_links(self):
    #     '''Get relevant article links to download.'''
    #     page = json.loads(requests.get(self.articles).content.decode())
    #     links = []
        
    #     for article in page['articles']:
    #         title = article['slug']
            
    #         if self.sport == 'nascar':
    #             if title.endswith('from-a-dfs-pro') or title.startswith('nascar-at') or title.startswith('projected-nascar-leaderboard'):
    #                 links.append(article['slug'])

    #         elif self.sport == 'golf':
    #             if title.endswith('from-a-dfs-pro') or title.endswith('has-surprising-picks-and-predictions'):
    #                 links.append(article['slug'])
                    
    #     return links
    
    
    # def update_articles(self):

    #     links = self._get_links()
    #     bucket = self.s3.Bucket(self.bucket_name)

    #     for obj in bucket.objects.all():
    #         if self.sport != 'golf':
    #             if 'sportsline' in obj.key and self.sport in obj.key:
    #                 key = obj.key.split('/')[-1]
    #                 if key in links:
    #                     links.remove(key)
    #         else:
    #             if 'sportsline' in obj.key and 'pga' in obj.key:
    #                 key = obj.key.split('/')[-1]
    #                 if key in links:
    #                     links.remove(key)
                
    #     #Open session and post the user_id and password
    #     with requests.Session() as session:
    #         post = session.post(self.login, data=self.payload)

    #         #open links
    #         for link in links:
    #             article = self.url.format(link)
    #             page = session.get(article)
    #             page = json.loads(page.text)

    #             #save article into s3 object
    #             obj = self.s3.Object(self.bucket_name, '{}/{}'.format(self.folder, link))
    #             obj.put(
    #                 Body=json.dumps(page['article'])
    #             )
    
    #             print(link) 

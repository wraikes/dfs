#log: [pid][projection][date_pulled]

import json
import logging
import requests
import boto3
import configparser
from datetime import datetime


class RawDataLine:
    '''Class to download & update Linestarapp Data into S3.
    
    Parameters:
        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
    
    Attributes:
        
    '''
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    parameters = {
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
        'mma': {
            'sport': 8,
            'pid_start': 237
        },
        'nascar': {
            'sport': 9,
            'pid_start': 209
        }
    }
    

    def __init__(self, sport):
        '''Initialize class'''
        self.sport = sport

        self.sport_id = self.parameters[self.sport]['sport']
        self.pid_start = self.parameters[self.sport]['pid_start']
        self.site = {'fd': 1, 'dk': 2}

        self.html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport={}&site={}&periodId={}'
        self.folder = '{}/linestarapp'.format(self.sport)


    def update_data(self):
        '''Update database with new sport data if applicable'''
        #delete projections data
        self._delete_projections()

        #get starting pid reference number for html download
        pid = self._get_max_pid() + 1
                
        #pull new json data and save to s3
        reach_max_pid = True

        while reach_max_pid:
            for site, site_num in self.site.items():
                data = self._pull_json_data(pid, site_num)
               
                #if (pid == 408 or pid == 606 or pid == 775 or pid == 1026) and self.sport == 'nba':
                #    pid += 1
                #    continue
                 
                #stop if no data
                try:
                    if not len(data['Ownership']['Salaries']) > 0:  #######is this accurate for all sports?
                       reach_max_pid = False
                       break
                except:
                    reach_max_pid = False
                    break
                
                #check if projections data and name as such
                projection = self._check_projection(data)
                object_name = self._get_string(site, pid, projection)
                
                #save new data
                obj = self.s3.Object(self.bucket.name, object_name)
                obj.put(
                    Body=json.dumps(data)
                )

                #print pid for monitoring
                print(site, pid)                 
            
            #update pid
            pid += 1


    def _delete_projections(self):
        '''If s3 object is a projection, then delete object'''
        for obj in self.bucket.objects.filter(Prefix=self.folder):
            if 'json' in obj.key and 'projections' in obj.key:
        
                #delete old projections data
                self.s3.Object('my-dfs-data', obj.key).delete()  
        
        
    def _get_max_pid(self):
        '''Get maximum pid from s3 bucket objects'''
        max_pid = self.pid_start
        
        for obj in self.bucket.objects.filter(Prefix=self.folder):
            if 'json' in obj.key:
                pid = self._get_pid(obj.key)
                
                if max_pid < pid:
                    max_pid = pid

        return max_pid
        

    def _pull_json_data(self, pid, site_num):
        '''Pull json data from html page'''
        html = self.html.format(self.sport_id, site_num, str(pid))
        page = requests.get(html).content.decode() 
        data = json.loads(page)       

        return data


    def _check_projection(self, data):
        #need to redo, as earlier games can throw this off (maybe use date?)
        '''Check if json data is projections (True) or historical (False)'''
        sum_pts = sum([x['PS'] for x in data['Ownership']['Salaries']])
        
        return sum_pts == 0


    def _get_pid(self, key):
        '''Get pid from object key'''
        pid = int(key.split('/')[-1].split('.')[0].split('_')[1])

        return pid


    def _get_string(self, site, pid, projection):

        if projection:
            object_name = '{}/{}_{}_projections.json'.format(self.folder, site, pid)
        else:
            object_name = '{}/{}_{}.json'.format(self.folder, site, pid)

        return object_name












#
#class SportslineData:
#    '''Class to download Sportsline articles into S3.
#    
#    Parameters:
#        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
#        
#    '''
#    #load s3 bucket details
#    s3 = boto3.resource('s3')
#    bucket_name = 'my-dfs-data'
#    bucket = s3.Bucket(bucket_name)
#
#    #load config parameters for sportsline
#    cfg = configparser.ConfigParser()
#    cfg.read('./raw_data_pull/etl.ini')
#    user_id = cfg['CREDENTIALS']['user_id']
#    password = cfg['CREDENTIALS']['password']
#
#    #load login details for sportsline
#    login = 'https://secure.sportsline.com/login'
#    payload = {
#        'dummy::login_form': '1',
#        'form::login_form': 'login_form',
#        'xurl': 'http://secure.sportsline.com/',
#        'master_product': '23350',
#        'vendor': 'sportsline',
#        'form_location': 'log_in_page',
#        'userid': user_id,
#        'password': password
#    }
#    
#    
#    def __init__(self, sport):
#        self.sport = sport if sport != 'pga' else 'golf' #confined to nhl, nascar, nfl, pga, nba, mlb
#        self.articles = 'https://www.sportsline.com/sportsline-web/service/v1/articleIndexContent?slug={}&limit=10000&auth=1'.format(self.sport)
#        self.url = 'https://www.sportsline.com/sportsline-web/service/v1/articles/{}?auth=1'
#        self.folder = '{}/sportsline'.format(sport)
#    
#    
#    def _get_links(self):
#        '''Get relevant article links to download.'''
#        page = json.loads(requests.get(self.articles).content.decode())
#        links = []
#        
#        for article in page['articles']:
#            title = article['slug']
#            
#            if self.sport == 'nascar':
#                if title.endswith('from-a-dfs-pro') or title.startswith('nascar-at') or title.startswith('projected-nascar-leaderboard'):
#                    links.append(article['slug'])
#
#            elif self.sport == 'golf':
#                if title.endswith('from-a-dfs-pro') or title.endswith('has-surprising-picks-and-predictions'):
#                    links.append(article['slug'])
#                    
#        return links
#    
#    
#    def update_articles(self):
#
#        links = self._get_links()
#        bucket = self.s3.Bucket(self.bucket_name)
#
#        for obj in bucket.objects.all():
#            if self.sport != 'golf':
#                if 'sportsline' in obj.key and self.sport in obj.key:
#                    key = obj.key.split('/')[-1]
#                    if key in links:
#                        links.remove(key)
#            else:
#                if 'sportsline' in obj.key and 'pga' in obj.key:
#                    key = obj.key.split('/')[-1]
#                    if key in links:
#                        links.remove(key)
#                
#        #Open session and post the user_id and password
#        with requests.Session() as session:
#            post = session.post(self.login, data=self.payload)
#
#            #open links
#            for link in links:
#                article = self.url.format(link)
#                page = session.get(article)
#                page = json.loads(page.text)
#
#                #save article into s3 object
#                obj = self.s3.Object(self.bucket_name, '{}/{}'.format(self.folder, link))
#                obj.put(
#                    Body=json.dumps(page['article'])
#                )
#    
#                print(link) 
#    

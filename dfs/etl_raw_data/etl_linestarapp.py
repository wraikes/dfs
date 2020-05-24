#log: [pid][projection][date_pulled]

import json
import logging
import requests
import boto3
import configparser

class LinestarappData:
    '''Class to download & update Linestarapp Data into S3.
    
    Parameters:
        sport: 'nascar', 'nfl', 'nba', 'mlb', 'nhl', or 'pga'
    
    Attributes:
        
    '''
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')

    # #load config parameters for linestarapp
    # cfg = configparser.ConfigParser()
    # cfg.read('./raw_data_pull/etl.ini')
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

        self.html = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetSalariesV4?sport={}&site={}&periodId={}'.format(self.sport_id)
        self.folder = '{}/linestarapp'.format(self.sport)


    def update_data(self):
        #open log file
        with open('~/dfs/logs/logs_linestarapp.json', 'r') as log_file:
            logs = json.load(log_file)

        '''Update database with new sport data if applicable'''
        #delete projections data
        self._delete_projections()

        #get starting pid reference number for html download
        pid = self._get_max_pid() + 1
                
        #pull new json data and save to s3
        while True:
            
            for site in self.site.keys():
            
                data = self._pull_json_data(pid, site)
               
                #if (pid == 408 or pid == 606 or pid == 775 or pid == 1026) and self.sport == 'nba':
                #    pid += 1
                #    continue
                
                #stop if no data
                try:
                    if not len(data['Ownership']['Salaries']) > 0:  #######is this accurate for all sports?
                        break
                except:
                    break
                
                #check if projections data and name as such
                projection = self._check_projection(data)
                current_date = datetime.datetime.now().strf('%m-%d-%Y')

                if projection:
                    object_name = '{}/{}_{}_projections.json'.format(self.folder, site, pid)
                    log = '{}_projection_{}'.format(site, pid, current_date)
                else:
                    object_name = '{}/{}_{}.json'.format(self.folder, site, pid)
                    log = '{}_{}_{}'.format(site, pid, current_date)
                
                #write log
                if log.split('_')[0] in [x.split('_')[:-1] for x in logs[self.sport]]:
                    logs[sport].append(log)

                #save new data
                obj = self.s3.Object(self.bucket.name, object_name)
                obj.put(
                    Body=json.dumps(data)
                )

                #update pid
                print(self.site, pid)                 
                pid += 1

        with open('~/dfs/logs/logs_linestarapp.json', 'w') as log_file:
            json.dump(logs, log_file)


    def _delete_projections(self):
        '''If s3 object is a projection, delete object'''
        for obj in self.bucket.objects.all():
            if self.sport in obj.key and 'json' in obj.key and 'projections' in obj.key and self.site in obj.key:
        
                #delete old projections data
                self.s3.Object('my-dfs-data', obj.key).delete()  
        
        
    def _get_max_pid(self):
        '''Get maximum pid from sport'''
        max_pid = self.pid_start
        
        for obj in self.bucket.objects.all():
            if self.sport in obj.key and 'json' in obj.key:
                pid = self._get_pid(obj.key)
                
                if max_pid < pid:
                    max_pid = pid

        return max_pid
        

    def _pull_json_data(self, pid, site):
        '''Pull json data from html page'''
        html = self.html.format(self.site[site]], str(pid))
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


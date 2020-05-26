#updates: only linestarapp data currently; does not search for prior logs; should be in json for one file
import json
import boto3

def create_logs():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-dfs-data')
    logs = {}

    for sport in ['pga', 'nascar']:
        logs[sport] = []

        for obj in bucket.objects.all():
            if sport in obj.key and 'json' in obj.key:
                
                object = s3.Object('my-dfs-data', obj.key)
                current_date = object.last_modified.strftime('%m-%d-%Y') 
                log = '{}_{}'.format(obj.key.split('.')[0].split('/')[-1], current_date)  
                
                if log not in logs[sport]:
                    logs[sport].append(log)
        
    with open('./logs_linestarapp.json', 'w') as log_file:
        json.dump(logs, log_file)


if __name__ == '__main__':
    create_logs()


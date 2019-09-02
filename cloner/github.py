import os 
import json
import pprint
import requests
import subprocess

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as f:
    CONFIG = json.load(f)


def get_users(filter=''):
    # set parameters
    auth = (CONFIG['GITHUB']['user'], CONFIG['GITHUB']['token'])
    params = {'per_page':100, 'page':1}

    users = []
    next_page = True
    repo_count = 0

    while next_page:
        response = requests.get('https://api.github.com/user/repos', auth=auth, params=params)
        response = response.json()

        # we can only get 100 repos per request
        if len(response) < 100:
            next_page = False
        else:
            params['page'] += 1
        
        for r in response:
            username = r['owner']['login']

            # ignore repos created by ourself
            if username == CONFIG['GITHUB']['user']:
                continue
            
            if filter in r['clone_url']:
                users.append(username)
    return users

# clone a specific folder in a github repo
def clone_folder(user, folder, output_dir):
    user_ta = CONFIG['GITHUB']['user']
    token_ta = CONFIG['GITHUB']['token']

    url = f'https://{user_ta}:{token_ta}@github.com/{user}/{folder}'
    script_path = os.path.join(os.path.dirname(__file__), 'git-pull.sh')

    subprocess.call(('sh', script_path, user, url, output_dir))
    
    
    




        
        

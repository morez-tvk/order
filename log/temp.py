import requests
import json
from requests.auth import HTTPBasicAuth
import pysolr


headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Authorization': 'Basic dXNlcl90YXZha29saWFuOjVESVNyZFdadU10Qw==',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://ha.dataak.com:8181/solr/',
    'Accept-Language': 'en-US,en;q=0.9,fa-IR;q=0.8,fa;q=0.7',
}
cookies = {
    'experimentation_subject_id': 'IjM4ZWEzM2E4LTU3YzktNDhmOS04OWVmLTQyZWUyOWUzN2FlNyI%3D--222533370bd01b274946b51f73b2fe66432fdf52',
    '__extfc': '1',
}

url_solr = '''http://ha.dataak.com:8181/solr/twitter'''
solr = pysolr.Solr(url_solr,auth=HTTPBasicAuth('app_twitter_tweet_consumer', 'UMBjAOv@&XZx'))
eof = False
batch_size = 1000
curser = '*'
total = 0
while not eof:
    params = (
        ('fl', 'post_id , Entities'),
        ('q', '*:*'),
        ('rows', batch_size),
        ('sort', 'post_id asc'),
        ('cursorMark', curser),
    )
    response = requests.get('http://ha.dataak.com:8181/solr/twitter/select',
                            params=params, auth=HTTPBasicAuth('user_tavakolian', '5DISrdWZuMtC'))
    # curser = response["nextCursorMark"]
    print('fetched')

    docs = json.loads(response.text)['response']['docs']
    tmp_curser = response.json()["nextCursorMark"]
    data = []
    for i in docs:
        if 'Entities' in i:
            ent = i['Entities']
            post_id = i['post_id']
            try:
                ent = json.loads(i['Entities'])
            except:
                ent = eval(i['Entities'])
            ent  = json.dumps(ent,ensure_ascii=False)
            data.append({"post_id" : post_id , "Entities"   : {"set":ent} })
    response = requests.post('http://ha.dataak.com:8181/solr/twitter/update', json=data , auth=HTTPBasicAuth('app_twitter_tweet_consumer', 'UMBjAOv@&XZx'))
    # print(response.status_code , response.json(),post_id)
    # curser = response["nextCursorMark"]
    # batch_size += 1000
    total += batch_size
    if curser != tmp_curser: curser = tmp_curser
    print(total)
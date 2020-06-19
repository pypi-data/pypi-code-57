import requests
from datetime import datetime


#get the node information from the oxidized server
#return None if nothing is required
def get_oxidized_nodeinfo(oxidized_url, name, ssl_verify=True):
    data = {'error': 'node not found'}

    if oxidized_url and oxidized_url != '':
        r = requests.get('{}/node/show/{}?format=json'.format(oxidized_url,name, verify=ssl_verify))
        if r.status_code == 200:
            data = r.json()
        else:
            data = {'error': 'node not found'}
    else:
        data = {'error': 'oxidized url not set or missing: URL:{}'.format(oxidized_url)}
    

    return data

def get_oxidized_nodeversion_list(oxidized_url, name, ssl_verify=True):
    data = {'error': 'node versions not found'}


    if oxidized_url and oxidized_url != '':
        # retrieve node versions
        r = requests.get('{}/node/version?node_full={}&format=json'.format(oxidized_url,name, verify=False))
        if r.status_code == 200:
            jdata = r.json()
            data = []
            for entry in data:
                vid = len(data) - data.index(entry)
                vdate = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S %z')
                version_data.append({'version': vid, 'date': vdate, 'author': entry['author']['name'], 'message':entry['message']})
        else:
            data = {'error': 'node versions not found'}
    else:
        data = {'error': 'oxidized url not set or missing: URL:{}'.format(oxidized_url)}

    return data
import queue
import datetime
import time
import threading
import requests
import json
from flask import request,g



buffer = queue.Queue()
flag = False

buffer_size=5
timeout=10
project_id = ""
auth_key=""
END_POINT_TO_SIMULATE_DB ="http://127.0.0.1:9000/"
time_to_refresh_cofg_file = 30
API_ENDPOINT=""

def set_buffer_size(size):
    global buffer_size
    buffer_size = size

def set_buffer_timeout(time):
    global timeout
    timeout = time
    
def set_API_ENDPOINT(endpoint):
    global API_ENDPOINT
    API_ENDPOINT = endpoint
    
def set_END_POINT_TO_SIMULATE_DB(db_endpoint):
    global END_POINT_TO_SIMULATE_DB
    END_POINT_TO_SIMULATE_DB = db_endpoint
    
def set_time_to_refresh(t):
    global time_to_refresh_cofg_file
    time_to_refresh_cofg_file = t
    
def set_project_id(projectId):
    global project_id
    project_id = projectId
    global API_ENDPOINT
    API_ENDPOINT= "https://sokt.io/" + project_id
    print(API_ENDPOINT)
    
def set_auth_key(key):
    global auth_key
    auth_key=key



""" with open('config.json') as json_data_file:
    config = json.load(json_data_file)
buffer_size = int(config['buffer_size'])
timeout = int(config['timer'])
API_ENDPOINT = config['END_POINT']
END_POINT_TO_SIMULATE_DB=config['END_POINT_TO_SIMULATE_DB']
time_to_refresh_cofg_file = int(config['time_to_refresh_cofg_file']) """

#fetching first time data from simulating_db api
response = requests.get(END_POINT_TO_SIMULATE_DB)
response=response.json()
includes = response[0]
levels=response[1]

def load_config_file():
    global includes
    global levels
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('LOADING CONFIG FILE', current_time)
    response = requests.get(END_POINT_TO_SIMULATE_DB)
    response=response.json()
    includes = response[0]
    levels=response[1]
    Timer.cancel()
    start_timer()

Timer=threading.Timer(time_to_refresh_cofg_file,load_config_file) 
    
def start_timer():
    print('inside timer')
    Timer=threading.Timer(time_to_refresh_cofg_file,load_config_file) 
    Timer.start()


count = 0


def hit_the_api():
    global buffer
    global count
    global API_ENDPOINT
    print('SENDING DATA TO DATABASE AT TIME ',
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data = (list(buffer.queue))
    buffer.queue.clear()
    print(data)
    r = requests.post(url=API_ENDPOINT, json=data)
    count=0 



def get_request_body(request):
    if (request.get_json() is not None):
        posted_data = request.get_json()    
    elif (request.form != {}):
        posted_data = request.form
    elif (request.content_type == 'text/plain'):
        posted_data = request.data
    else:
        posted_data=None
    return posted_data    
    
    
t = threading.Timer(timeout, hit_the_api)

def main_logic_for_sending_logs(message):
    list = {}
    list['message'] = (message)
    global count
    global t
    global buffer
    count = count + 1
    if count == 1:
        t = threading.Timer(timeout, hit_the_api)
        t.start()
    if(buffer.qsize()>=buffer_size-1):
        buffer.put(list)
        t.cancel()
        hit_the_api()    
    else:
        buffer.put(list)


def sendLog(message):
    global flag
    global includes
    global levels
    print('inside send log method')

    if flag == False:
            flag = True
            start_timer()  

    #if isinstance(message,dict):
    if 'level' in message.keys():
        level = message['level']
        if (len(levels) == 1 and levels[0] == '*'):
            main_logic_for_sending_logs(message)
        elif (level in levels):
            main_logic_for_sending_logs(message)
    else:     
        #filtering logic
        print('inside else')
        print(includes, len(includes))
        print(levels, len(levels))
        if (len(includes) == 1 and includes[0] == '*'):
            main_logic_for_sending_logs(message)
        elif(request.path  in includes):
            main_logic_for_sending_logs(message)


def info(message):
    level = 'INFO'
    list = {}
    list['timestamp']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list['level']=level
    list['data']=message
    print(list)
    sendLog(list)
def error(message):
    level = 'ERROR'
    list = {}
    list['timestamp']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list['level']=level
    list['data']=message
    sendLog(list)
def warn(message):
    level = 'WARN'
    list = {}
    list['timestamp']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list['level']=level
    list['data']=message
    sendLog(list)




def log_request(response):
    print('after every request')
    now = time.time()
    duration = round(now - g.start, 2)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = {}
    log_params['method']= request.method
    log_params['path'] =request.path
    log_params['status']=response.status_code
    log_params['duration']=duration
    log_params['time']=timestamp
    log_params['ip']=ip
    log_params['host']=host
    log_params['params']=args

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params['request_id']= request_id

    log_params['request_body'] =get_request_body(request)
    headers=[]
    for h in response.headers:
        headers.append(h)
    log_params['resonse_headers']=headers
    log_params['response_body']= response.data.decode("utf-8")
    print((log_params))
    print(type(log_params))
    #sendLog(json.loads(json.dumps(log_params)))
    sendLog(log_params)
    return response
    
import stomp
from stomp.exception import ConnectFailedException
import rfApiTestLibrary.log as log

def send_to_queue(query_or_topic_name, msg, host, port=61613, username=None, password=None):
    '''
    通过stomp协议向activeMQ发送消息。
    :param query_or_topic_name: string类型。activeMQ的队列名或者主题名。
    :param msg: string类型。需要发送的消息。
    :param host: string类型,activeMQ的域名或者IP地址。
    :param port: int类型, activeMQ stomp端口,注意是stomp协议端口。
    :param username: string类型。activeMQ的broker用户名。
    :param password: string类型。activeMQ的broker的密码。
    '''
    try:
        conn = stomp.Connection10([(host, port)])
        conn.start()
        if username is None or password is None:
            conn.connect()
        else:
            conn.connect(username, password, wait=True)
        conn.send(query_or_topic_name, msg)
        conn.disconnect()
        log.info('向activeMQ['+host+':'+str(port)+']queue或者topic['+ query_or_topic_name +']发送消息'+msg,html=True, also_console=True)
    except ConnectFailedException as e:
        raise AssertionError("连接activeMQ失败,请确认activeMQ地址或者stomp端口或者broker的用户名或者密码是否正确")

'''
Documentation: 处理websocket的方法。不要用此文件方法做任何长连接测试。
'''
from websocket import create_connection
import rfApiTestLibrary.log as logger

isWriteHtml=True
also_console=True

def open_connection(url,timeout=None,header=None):
    '''
    创建websocket连接.
    :param url: string类型。比如ws://localhost:8080/aa/bb?cc=11&dd=22
    :param timeout: int类型,过期时间，单位秒。
    :param header: 请求头,字典或者列表类型
    :return: 连接句柄
    '''
    # ws=create_connection(url,timeout=timeout,header=header)
    ws = create_connection(url)
    logger.info("创建websocket连接:"+url ,html=isWriteHtml, also_console=also_console)
    return ws

def send(ws,msg):
    '''
    发送消息。
    :param ws: websocket连接句柄
    :param msg: string类型,发送的消息。
    :return: string类型。
    '''
    ws.send(msg)
    logger.info("发送消息: %s" % msg, html=isWriteHtml, also_console=also_console)
    result = ws.recv()
    logger.info("收到消息: %s" % result, html=isWriteHtml, also_console=also_console)
    return result

def close(ws):
    '''
    关闭websocket连接
    :param ws:websocket连接句柄
    '''
    ws.close()

def send_msg(url,msg,timeout=None,header=None):
    '''

    :param url: string类型。比如ws://localhost:8080/aa/bb?cc=11&dd=22
    :param msg: string类型,发送的消息。
    :param timeout: int类型,过期时间，单位秒。
    :param header: 请求头,字典或者列表类型
    :return: string类型，收到的结果。
    '''
    ws=open_connection(url,timeout=timeout,header=header)
    result=send(ws,msg)
    close(ws)
    return result
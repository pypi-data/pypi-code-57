'''
Documentation: 处理rabitMQ的API。
引用包名是atApiBasicLibrary，引用本python文件，请使用Library  atApiBasicLibrary/rabitmqLib.py。
'''

import pika
import atApiBasicLibrary.log as logger

def _at_get_rabitmq_connection(host="127.0.0.1",port=5672, username="guest",password="guest"):
    '''
    通过标准配置连接rabitMQ。底层方法。
    :param host: rabitMQ的IP或者域名。string类型。默认是127.0.0.1。
    :param port: rabitMQ的端口号，int类型。默认是5672。
    :param username: rabitMQ的用户名.默认值是guest.String类型
    :param password: rabitMQ的密码。默认值是guest.String类型
    :return: rabitMQ connection
    '''
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    return connection

def at_publish_message(message, host="127.0.0.1",port=5672, username="guest",password="guest",exchange="", routing_key=""):
    '''
    向exchange或者queue发送消息。如果是fanout向exchange发送消息，设置routing_key为空""。如果是AMQP default,直接向queue发送消息,请设置exchange为空字符""。
    注意如果输入不存在的exchange或者queue，不会报任何错。
    :param message: 发送的消息。String类型。必填字段。
    :param host: rabitMQ的IP或者域名。string类型。默认是127.0.0.1。
    :param port: rabitMQ的端口号，int类型。默认是5672。
    :param username: rabitMQ的用户名.默认值是guest.String类型
    :param password: rabitMQ的密码。默认值是guest.String类型
    :param exchange: rabitMQ的交换机，String类型。默认是空字符串。
    :param routing_key: rabitMQ的队列，String类型。默认是空字符串。

     Examples:
        |         关键字      |  message   |    host    | port  | username  |  password |  exchange | routing_key |
        | at publish message | 消息        | 127.0.0.1 | 5672  |  guest    |  guest     |   abdsa   | fasaffafa   |
    '''
    connection= _at_get_rabitmq_connection(host=host,port=port, username=username,password=password)
    channel = connection.channel()
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    if exchange==""  and routing_key!="":
        logger.info('向RabitMQ ['+host+':'+str(port)+']的routing_key:'+str(routing_key)+' 发送消息: '+ message, html=True, also_console=True)
    elif exchange!=""  and routing_key=="":
        logger.info('向RabitMQ [' + host + ':' + str(port) + ']的exchange:' + str(exchange) + ' 发送消息: ' + message,html=True, also_console=True)
    else:
        logger.info('向RabitMQ [' + host + ':' + str(port) + ']的exchange:' + str(exchange)+ ', routing_key:'+str(routing_key)+ ' 发送消息: ' + message, html=True, also_console=True)
    connection.close()

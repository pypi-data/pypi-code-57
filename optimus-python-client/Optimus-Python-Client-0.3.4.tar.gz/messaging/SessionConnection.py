import pika
from pika import channel
from pika.channel import Channel


def getChannel():
    return channel.Channel


def test():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False, exclusive=False,
                          consumer_tag=None, arguments=None, )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()


class SessionConnection(object):
    pass


def getInstance(sessionConnection=None):
    if sessionConnection is None:
        sessionConnection = SessionConnection7()
    return sessionConnection


def getConnection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    return connection


class SessionConnection7(object):
    sessionConnection = SessionConnection()
    channel = Channel

    def getChannel(self):
        return self.channel

    def __init__(self):
        self.sessionConnection = SessionConnection7
        connection = getConnection()
        channel = connection.channel()
        # can specify various properties that control the durability of the queue and its contents, and the level of
        # sharing for the queue.
        channel.queue_declare(queue='hello')
        channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        print("[x] Sent 'Hello World!'")
        connection.close()


if __name__ == '__main__':
    SessionConnection7()
    test()
    print(getChannel())


class UserInfo(object):
    username = str
    password = str

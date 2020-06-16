from threading import Lock

from messaging.SessionConnection import getInstance, getConnection, getChannel

lock = Lock()


def consumeMessage(routingKey):
    lock.acquire()
    try:
        channel = getChannel()

        getResponse = channel.basic_get(routingKey, False)
        return getResponse.__str__
    except Exception as error:
        return error


def queueHasAMessage(queue_name):
    instance = getInstance().getChannel()
    connection = getConnection().channel()
    queue = connection.queue_declare(queue=queue_name).method.message_count
    return queue > 0


class SessionQueueReader:
    pass


if __name__ == '__main__':
    consumeMessage('hello')
    print(queueHasAMessage('hello'))

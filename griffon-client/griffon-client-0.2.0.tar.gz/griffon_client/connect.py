import socketio
import inspect
import json
from urllib.parse import urlencode


#************************************************************************
#* Private Functions
#***********************************************************************/

def normalize_consumer(consumer):

    if consumer is None:
        return {'or': []}

    elif isinstance(consumer, str):

        return {'or': [consumer]}

    elif isinstance(consumer, list):

        return {'or': consumer}

    else:
        return consumer

def normalize_array(producer):

    if producer is None:
        return []

    elif not isinstance(producer, list):
        return [producer]

    else:
        return producer


#************************************************************************
#* Public Functions
#***********************************************************************/


class Client():


    def __init__(self, uri=None, username=None, password=None, task=None, environment='default', consume=None, produce=None, channels=['default'], gather=False):
        
        self.channels=channels

        print(f'connecting to server at {uri}')


        consume = normalize_array(consume)

        self.consumers = {}

        self.gatherer = None

        config = {}

        config['and' if gather is True else 'or'] = consume

        consume = config

        query = json.dumps({
            'username': username,
            'password': password,
            'operator': task,
            'environment': environment,
            'consume': normalize_consumer(consume),
            'produce': normalize_array(produce),
            'channels': normalize_array(channels),
        })



        self.socket = socketio.AsyncClient()


        @self.socket.on('connect')
        async def on_connect():
            print('Successfully connected.')


        class task():
            def __init__(self, socket, topic, topics, data, payload):
                self.payload = payload
                self.data = data
                self.topics = topics
                self.topic = topic
                self.socket = socket


            def produce(self, topic=None, data=None):

                if topic is None:
                    raise Exception('Producers must include a topic.')
                if data is None:
                    raise Exception("'data', must not be 'None'.")

                production_payload = {
                    'topic': topic,
                    'stream_id': self.payload['stream_id'],
                    'channel': self.payload['channel'],
                    'data': data,
                }

                print(f'Producing Topic: {topic}')

                self.socket.emit('production', production_payload)




        @self.socket.on('consumption')
        async def consumption(payload):


            if self.gatherer is not None:

                print(f'Consuming Topics: {payload["topics"]}')

                if inspect.iscoroutinefunction(consumer):

                    await self.gatherer(task(self.socket, None, payload['topics'], payload['data'], payload))
                
                else:
                    self.gatherer(task(self.socket, None, payload['topics'], payload['data'], payload))
            
            else:

                for topic in payload['topics']:


                    consumer = None

                    if topic in self.consumers:
                        consumer = self.consumers[topic]

                    elif '*' in self.consumers:
                        consumer = self.consumers['*']
                    
                    if consumer is not None:

                        print(f'Consuming Topic: {topic}')

                        if inspect.iscoroutinefunction(consumer):

                            await consumer(task(self.socket, topic, payload['topics'], payload['data'][topic], payload))
                        
                        else:
                            consumer(task(self.socket, topic, payload['topics'], payload['data'][topic], payload))

                    else:
                        raise Exception("No consumer found for registerd topic.")


        @self.socket.on('error')
        async def on_error(error):
            print(error)

        @self.socket.on('info')
        async def on_info(info):
            print(info)

        result = None
        while result is None:
            try:
                self.socket.connect(f'{uri}?init={query}')
                result = True
                self.socket.sleep(3)

            except socketio.exceptions.ConnectionError as e:
                result = None
                print(f'failed to connect to server at {uri}')
                self.socket.sleep(3)
                pass


    def consume(self, topics):

        def register_consumers(func):

            nonlocal topics

            topics = normalize_array(topics)

            for topic in topics:

                if topic in self.consumers or '*' in self.consumers:
                    raise Exception(f'Consumer for topic {topic} has already been registered.')

                self.consumers[topic] = func

        if callable(topics):
            func = topics
            topics = ['*']
            register_consumers(func)

        else:
            return register_consumers




    def gather(self, func):

        if len(self.consumers.keys()) > 0:
            raise Exception(f'Gather listens for all topics and can not be used with consume.')
        
        self.gatherer = func


    def produce(self, topic=None, channel=None, data=None):

        if channel is None and len(self.channels) == 1 and self.channels[0] == 'default':
            channel = 'default'

        if topic is None:
            raise Exception('Producers must include a topic.')
        if channel is None:
            raise Exception('Raw production must include a channel.')
        if data is None:
            raise Exception("'data', must not be 'None'.")

        print(f'Producing Topic: {topic}')

        self.socket.emit('production', {
            'topic': topic,
            'channel': channel,
            'data': data,
        })

import functools as fc
import asyncio
import logging
import math
import codecs
import ujson as json
from networktools.time import timestamp
from networktools.colorprint import gprint, bprint, rprint
from data_amqp import AMQPData
from tasktools.taskloop import coromask, renew, simple_fargs, simple_fargs_out


"""
La implementación de una clase heredera

Signatures:
==========

- a :: array
- s :: string
- v :: variant
- a{sv} :: un diccionario

ref:: https://www.gkbrk.com/2018/02/simple-dbus-service-in-python/
"""


def convert_dict2json(msg):
    dt = msg.get('properties').get('dt').isoformat()
    dt_rdb = msg.get('properties').get('DT_GEN').isoformat()
    return dbus.Dictionary({
        'features': dbus.Array(
            dbus.Dictionary(msg.get('features')[0], signature="sv")),
        'type': msg.get('type'),
        'dt': dt,
        'properties': dbus.Dictionary(msg.get('properties'), signature='sv')
    }, signature='sv')



"""

DBusConnection
"""


class RMQEngine:
    def __init__(self, *args, **kwargs):
        self.__status = False
        self.amqp = None
        if kwargs.get('amqp', False):
            try:
                self.amqp_opt = kwargs['amqp']
                self.amqp = AMQPData(**kwargs)
                self.__status = True
            except Exception as e:
                self.__status = False
                raise e

    @property
    def status(self):
        return self.__status

    def enu_data(self, msg):
        try:
            self.amqp.manage_json_data(msg)
        except Exception as e:
            raise e

    def solo_data(self, msg):
        try:
            self.amqp.manage_json_data(msg.get('data',{}))
        except Exception as e:
            raise e



        
class DataManager:
    def __init__(self, queue, engine_opts, step=0.1, *args, **kwargs):
        self.step = step
        self.queue = queue
        self.engine_opts = engine_opts
        print("Channels", list(engine_opts.keys()))
        self.engine = False

    def create_rmq(self, channel, engine):
        try:
            value_dict = self.engine_opts.get(channel)
            rmq = RMQEngine(**value_dict)
            engine.update({channel: rmq})
            return rmq
        except Exception as e:
            print("Can't create RMQ connection %s" % e)
            raise e

    async def cycle(self, *args, **kwargs):
        engine = args[0]
        v = args[1]
        init_set = args[2]
        queue = self.queue
        await asyncio.sleep(1)
        if v == 0:
            engine = {}
            try:
                added_set = set()
                for channel in init_set:
                    print("Init conection to channels rmq", channel)
                    value_dict = self.engine_opts.get(channel)
                    rmq = RMQEngine(**value_dict)
                    engine.update({channel: rmq})
                    added_set.add(channel)
                for item in added_set:
                    init_set.remove(item)
                v += 1
            except Exception as e:
                print("Error al intentar conectar rabbitmq %s" % e)
                v = 0
            return [engine, v, init_set], kwargs
        else:
            if engine:
                if not queue.empty():
                    for i in range(queue.qsize()):
                        msg = queue.get()
                        if type(msg) == dict:
                            # get channel from msg, to direct the msg
                            channel = msg.get('channel', None)
                            if channel in engine:
                                try:
                                    if engine.get(channel).status:
                                        # select the dbus channel and send data
                                        if channel=='earlybird':
                                            engine.get(channel).solo_data(msg)
                                        else:
                                            engine.get(channel).enu_data(msg)
                                except Exception as ex:
                                    print("Error en comunicar %s, channel %s" %
                                          (ex, channel))
                                    engine.amqp.connect()
                                    init_set.add(channel)
                                    v = 0
                        queue.task_done()
            await asyncio.sleep(self.step)
            return [engine, v, init_set], kwargs

    def task_cycle(self):
        loop = asyncio.get_event_loop()
        # engine = {channel:
        #          for channel, value_dict in self.engine_opts.items()}
        rprint("#"*30)
        bprint("Task Cycle Ok")
        rprint("#"*30)
        v = 0
        init_set = set(self.engine_opts.keys())
        coroutine_future = coromask(
            self.cycle, [{}, v, init_set], {}, simple_fargs_out)
        task = loop.create_task(coroutine_future)
        task.add_done_callback(
            fc.partial(renew, task, self.cycle, simple_fargs_out))
        if not loop.is_running():
            loop.run_forever()

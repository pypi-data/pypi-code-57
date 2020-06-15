################################################################################
# Copyright (C) 2016-2020 Abstract Horizon
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Daniel Sendula - initial API and implementation
#
#################################################################################


import os
import sys
import re
import time
import random
import traceback
import threading
import paho.mqtt.client as mqtt
import multiprocessing

client = None

_name = "undefined"
_host = None
_port = 1883
_clusterId = None

_client_loop = 0.0005
_loop_sleep = 0.002

DEBUG_SUBSCRIBE = False
PRIORITY_LOW = 0
PRIORITY_NORMAL = 1
PRIORITY_HIGH = 2


def do_nothing():
    pass


_process_id = "unknown"
_on_connected = do_nothing
_on_stop = do_nothing
_connected = False

_subscribers = []
_regex_text_to_lambda = {}
_regex_binary_to_lambda = {}

_collect_stats = False

_stats = [[0, 0, 0]]
_received = False


def _set_cluster_id(c_id):
    global _clusterId

    _clusterId = c_id


def get_cluster_id():
    if _clusterId is not None:
        return _clusterId
    else:
        return "master"


def _add_send_message():
    current_stats = _stats[len(_stats) - 1]
    current_stats[1] = current_stats[1] + 1


def _add_received_message():
    current_stats = _stats[len(_stats) - 1]
    current_stats[2] = current_stats[2] + 1


def is_connected():
    return _connected


def get_connection_details():
    return _host, _port


def publish(topic, message):
    if _connected:
        client.publish(topic, message)
        if _collect_stats:
            _add_send_message()


def subscribe(topic, method):
    _subscribers.append(topic)
    regex_string = "^" + topic.replace("+", "([^/]+)").replace("#", "(.*)") + "$"
    regex = re.compile(regex_string)

    has_self = hasattr(method, '__self__')
    all_args_count = (3 + (1 if has_self else 0))

    has_groups = method.__code__.co_argcount == all_args_count
    _regex_text_to_lambda[regex] = (has_groups, method)

    if DEBUG_SUBSCRIBE:
        print("*** stored method " + str(method) + " with has group " + str(has_groups) + " and it self is " + str(has_self) + ", expected arg no " + str(all_args_count))

    if _connected:
        client.subscribe(topic, 0)


def subscribe_binary(topic, method):
    _subscribers.append(topic)
    regex_string = "^" + topic.replace("+", "([^/]+)").replace("#", "(.*)") + "$"
    regex = re.compile(regex_string)

    has_self = hasattr(method, '__self__')
    all_args_count = (3 + (1 if has_self else 0))

    has_groups = method.__code__.co_argcount == all_args_count

    _regex_binary_to_lambda[regex] = (has_groups, method)

    if DEBUG_SUBSCRIBE:
        print("*** stored method " + str(method) + " with has group " + str(has_groups) + " and it self is " + str(has_self) + ", expected arg no " + str(all_args_count))

    if _connected:
        client.subscribe(topic, 0)


def unsubscribe(topic):
    if _connected:
        client.unsubscribe(topic)

    regex_string = "^" + topic.replace("+", "([^/]+)").replace("#", "(.*)") + "$"
    regex = re.compile(regex_string)

    if regex in _regex_binary_to_lambda:
        del _regex_binary_to_lambda[regex]

    if regex in _regex_text_to_lambda:
        del _regex_text_to_lambda[regex]


def subscribed_method(topic):
    regex_string = "^" + topic.replace("+", "([^/]+)").replace("#", "(.*)") + "$"
    regex = re.compile(regex_string)

    if regex in _regex_text_to_lambda:
        return _regex_text_to_lambda[regex]

    if regex in _regex_binary_to_lambda:
        return _regex_binary_to_lambda[regex]

    return None


def _send_stats():
    msg = ""
    for stat in _stats:
        msg = msg + str(stat[0]) + "," + str(stat[1]) + "," + str(stat[2]) + "\n"

    publish("exec/" + _process_id + "/stats/out", msg)


def _handle_stats(_topic, payload, _groups):
    global _collect_stats

    if "start" == payload:
        _collect_stats = True
    elif "stop" == payload:
        _collect_stats = False
    elif "read" == payload:
        _send_stats()


def _handle_system(_topic, payload, _groups):
    def wait_for_process_stop():
        print("Confirming stop for service " + _process_id)
        publish("exec/" + _process_id + "/system/stop", "stopped")
        client.loop(0.001)
        if _on_stop is not None:
            print("Invoking stop callback for service " + _process_id)
            _on_stop()

        loop(0.5)

        print("Stopping service " + _process_id)
        os._exit(0)

    if payload.strip() == "stop":
        thread = threading.Thread(target=wait_for_process_stop, daemon=True)
        thread.start()


def _on_disconnect(_mqtt_client, _data, _rc):
    _connect()


def _on_connect(mqtt_client, _data, _flags, rc):
    global _connected
    if rc == 0:
        _connected = True
        for subscriber in _subscribers:
            mqtt_client.subscribe(subscriber, 0)
        if _on_connected is not None:
            _on_connected()

    else:
        print("ERROR: Connection returned error result: " + str(rc))
        sys.exit(rc)


def _on_message(_mqtt_client, _data, msg):
    global _received

    _received = True

    topic = msg.topic

    if _collect_stats:
        _add_received_message()

    try:
        for regex in _regex_text_to_lambda:
            matching = regex.match(topic)
            if matching:
                payload = str(msg.payload, 'utf-8')

                invoke_handler(topic, payload, matching.groups(), _regex_text_to_lambda[regex])

                # (has_groups, method) = _regexTextToLambda[regex]
                # if has_groups:
                #     method(topic, payload, matching.groups())
                # else:
                #     method(topic, payload)

                return

        for regex in _regex_binary_to_lambda:
            matching = regex.match(topic)
            if matching:
                invoke_handler(topic, msg.payload, matching.groups(), _regex_binary_to_lambda[regex])

                # (has_groups, method) = _regexBinaryToLambda[regex]
                # if has_groups:
                #     method(topic, msg.payload, matching.groups())
                # else:
                #     method(topic, msg.payload)
                # return

    except Exception as ex:
        print("ERROR: Got exception in on message processing; " + str(ex) + "\n" + ''.join(traceback.format_tb(ex.__traceback__)))


def invoke_handler(topic, message, groups, details):
    has_groups, method = details

    if has_groups:
        method(topic, message, groups)
    else:
        method(topic, message)


def _reconnect():
    try:
        client.reconnect()
    except Exception:
        pass


def _connect():
    global _connected
    _connected = False

    if client is not None:
        try:
            client.disconnect()
        except Exception:
            pass

    # print("DriveController: Connecting to rover " + str(selectedRover + 2) + " @ " + roverAddress[selectedRover] + "...");

    client.connect_async(_host, _port, 60)
    thread = threading.Thread(target=_reconnect)
    thread.daemon = True
    thread.start()


def on_disconnect(_mqtt_client, _data, _rc):
    _connect()


def init(name, unique=False, on_connected=None, on_stop=None, wait_to_connect=True, host='localhost', port=1883):
    global client, _connected, _on_connected, _on_stop, _name, _process_id, _host, _port, _loop_sleep, _client_loop

    _on_connected = on_connected
    _on_stop = on_stop

    if unique:
        name += "-" + str(random.randint(10000, 99999))

    _name = name
    client = mqtt.Client(name)

    client.on_disconnect = _on_disconnect
    client.on_connect = _on_connect
    client.on_message = _on_message

    if 'PYROS_MQTT' in os.environ:
        pyros_mqtt_broker = os.environ['PYROS_MQTT']
        host_port = pyros_mqtt_broker.split(":")
        if len(host_port) == 1:
            host = host_port[0]
        elif len(host_port) > 1:
            host = host_port[0]
            try:
                port = int(host_port[1])
            except Exception:
                pass

    if 'PYROS_CLUSTER_ID' in os.environ:
        _set_cluster_id(os.environ['PYROS_CLUSTER_ID'])

    if host is not None:
        connect(host, port, wait_to_connect)

    if len(sys.argv) > 1:
        _process_id = sys.argv[1]
        cId = get_cluster_id()
        if cId == "master":
            print("Started " + _process_id + " process on master pyros.py. Setting up pyroslib...")
        else:
            print("Started " + _process_id + " process on " + get_cluster_id() + " clustered pyros.py. Setting up pyroslib...")
        subscribe("exec/" + _process_id + "/stats", _handle_stats)
        subscribe("exec/" + _process_id + "/system", _handle_system)
    else:
        print("No processId argument supplied.")

    _host = host
    _port = port

    if multiprocessing.cpu_count() == 1:
        _loop_sleep = 0.004
        _client_loop = 0.001
    else:
        _loop_sleep = 0.002
        _client_loop = 0.0005


def connect(host, port=1883, wait_to_connect=True):
    global _host, _port

    _host = host
    _port = port

    _connect()

    if wait_to_connect:
        print(f"    {_name} waiting to connect to broker @{host}:{port} ...")
        while not _connected:
            loop(0.02)
        print(f"    {_name} connected to broker.")


def sleep(delta_time):
    loop(delta_time)


def loop(delta_time, inner=None, loop_sleep=None, priority=PRIORITY_NORMAL):
    global _received

    if loop_sleep is None:
        if priority == PRIORITY_LOW:
            loop_sleep = 0.05
        else:
            loop_sleep = _loop_sleep

    def client_loop():
        try:
            client.loop(_client_loop)  # wait for 0.5 ms
        except BaseException as ex:
            print("MQTT Client Loop Exception: " + str(ex) + "\n" + ''.join(traceback.format_tb(ex.__traceback__)))

    current_time = time.time()

    _received = False
    client_loop()

    until = current_time + delta_time
    while current_time < until:
        if _received:
            _received = False
            client_loop()
            current_time = time.time()
        else:
            time.sleep(loop_sleep)  # wait for 2 ms
            current_time = time.time()
            if current_time + _client_loop < until:
                client_loop()
                current_time = time.time()


def forever(delta_time, outer=None, inner=None, loop_sleep=None, priority=PRIORITY_NORMAL):
    global _received

    current_time = time.time()
    next_time = current_time

    while True:
        if _collect_stats:
            _stats.append([next_time, 0, 0])
            if len(_stats) > 100:
                del _stats[0]

        next_time = next_time + delta_time
        try:
            if outer is not None:
                outer()
        except BaseException as ex:
            print("ERROR: Got exception in discovery loop; " + str(ex) + "\n" + ''.join(traceback.format_tb(ex.__traceback__)))

        current_time = time.time()

        sleep_time = next_time - current_time
        if sleep_time < _loop_sleep:
            next_time = current_time

            _received = False
            client.loop(_client_loop)  # wait for 0.1 ms
            count = 10  # allow at least 5 messages
            while count > 0 and _received:
                _received = True
                count -= 1
                client.loop(_client_loop)  # wait for 0.1 ms

        else:
            loop(sleep_time, inner=inner, loop_sleep=loop_sleep, priority=priority)

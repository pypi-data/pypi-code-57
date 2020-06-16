"""
.. module:: zerynthzdmclient

.. _lib.zerynth.zdmclient:

**********************
ZDM Client Python
**********************

The Zerynth ZDM Client is a Python implementation of a client of the ZDM.
It can be used to emulate a Zerynth device and connect it to the ZDM.

    """

import json
import logging
import time
import datetime

from .mqtt import MQTTClient
from ..logging import MyLogger

logger = MyLogger().get_logger()

ENDPOINT = "mqtt.zdm.zerynth.com"
PORT = 1883


class ZDMClient:
    """
================
The ZDMClient class
================

.. class:: ZDMClient(device_id, jobs=None, endpoint=ENDPOINT, verbose=False, time_callback=None)

    Creates a ZDM client instance with device id :samp:`device_id`. All other parameters are optional and have default values.

    * :samp:`device_id` is the id of the device.
    * :samp:`jobs` is the dictionary that defines the device's available jobs (default None).
    * :samp:`endpoint` is the url of the ZDM broker (default rmq.zdm.zerynth.com).
    * :samp:`verbose` boolean flag for verbose output (default False).
    * :samp:`time_callback`, is a function accepting that will be called when timestamps are received after time_request


    """

    def __init__(self, device_id, jobs=None, endpoint=ENDPOINT, verbose=False, time_callback=None):
        self.mqtt_id = device_id
        self.jobs = jobs
        self.zdm_endpoint = endpoint
        self.mqttClient = MQTTClient(mqtt_id=device_id)

        self._time_callback = time_callback

        self.data_topic = '/'.join(['j', 'data', device_id])
        self.up_topic = '/'.join(['j', 'up', device_id])
        self.dn_topic = '/'.join(['j', 'dn', device_id])
        if verbose:
            logger.setLevel(logging.DEBUG)

    def id(self):
        """
.. method:: id(pw)

        Return the device id.
        """
        return self.mqtt_id

    def connect(self):
        """
.. method:: connect()

        Connect your device to the ZDM. You must set device's password first. It also enable your device to receive incoming messages.
        """
        for _ in range(5):
            try:
                logger.info("ZDMClient.connect attempt")
                self.mqttClient.connect(host=self.zdm_endpoint, port=PORT)
                break
            except Exception as e:
                logger.error("ZDMClient.connect", e)
                pass
        time.sleep(2)
        if not self.mqttClient.connected:
            raise Exception("Failed to connect")

        self._subscribe_down()
        self._request_status()
        self._send_manifest()

    def set_password(self, pw):
        """
    .. method:: set_password(pw)

        Set the device password to :samp:`pw`. You can generate a password using the ZDM, creating a key for your device
        """
        self.mqttClient.set_username_pw(self.mqtt_id, pw)

    def publish_data(self, tag, payload):
        """
    .. method:: publish_data(tag, payload)

        Publish a message to the ZDM.

        * :samp:`tag`, is a label for the device's data into your workspace. More than one device can publish message to the same tag
        * :samp:`payload` is the message payload, represented by a dictionary
        """
        topic = self._build_ingestion_topic(tag)
        self.mqttClient.publish(topic, payload)
        logger.info("Message published correctly. Msg: {}, topic:{}".format(payload, topic))

    def _subscribe_down(self):
        logger.debug("ZdmClient._subscribe_down subscribed to topic: {}".format(self.dn_topic))
        self.mqttClient.subscribe(self.dn_topic, callback=self._handle_dn_msg)

    def _request_status(self):
        msg = {
            'key': '#status',
            'value': {}
        }
        self._publish_up(msg)
        logger.debug("Status requested")

    def request_timestamp(self):
        msg = {
            'key': '#now',
            'value': {}
        }
        self._publish_up(msg)
        logger.debug("Timestamps requested")

    def _send_manifest(self):
        if self.jobs:
            payload = {
                'key': '__manifest',
                'value': [k for k in self.jobs]
            }

            self.mqttClient.publish(self.up_topic, json.dumps(payload))
            logger.debug("Sent manifest correctly. Payload: {}".format(payload))
        else:
            logger.debug("No custom Jobs.")

    def _publish_up(self, payload):
        topic = self.up_topic
        self.mqttClient.publish(topic, payload)
        logger.debug("Msg published on UP topic correctly. Msg: {}, topic:{}".format(payload, topic))

    def _handle_delta_status(self, arg):
        logger.debug("Received a delta status. Msg:{}".format(arg))

        if ('expected' in arg) and (arg['expected'] is not None):
            if '@fota' in arg['expected']:
                logger.warning("FOTA is not supported on ZdmClient")
            else:
                # handle other keys
                for expected_key in arg['expected']:
                    value = arg['expected'][expected_key]['v']

                    if expected_key[0] == '@':
                        if expected_key[1:] in self.jobs:
                            try:
                                res = self.jobs[expected_key[1:]](self, arg)
                                job_response = {
                                    "key": expected_key,
                                    "value": {"status": "done", "result": res}
                                }
                                self._publish_up(json.dumps(job_response))
                                logger.info("Job {} executed succesfully. Result: {}".format(expected_key[1:], res))
                            except Exception as e:
                                logger.error("ZdmClient.handle_job_request", e)
                                res = 'exception'

    def _handle_dn_msg(self, client, data, msg):
        payload = json.loads(msg.payload.decode("utf-8"))
        logger.debug("AdmClient._handle_dn_msg receive message: {}".format(payload))
        try:
            if "key" not in payload:
                raise Exception(
                    "The key  is not present into the job payload {}".format(payload))
            if "value" not in payload:
                raise Exception(
                    "The value  is not present into the job payload {}".format(payload))

            method = payload["key"]
            value = payload["value"]
            if "args" in value:
                args = value["args"]
            else:
                args = {}

            if method.startswith('@'):
                method = method[1:]
                if method in self.jobs:
                    result = self.jobs[method](self, args)
                    logger.info("[{}] job {} executed with result res:{} ".format(
                        self.mqtt_id, method, result))

                    job_response = {
                        "key": "@" + method,
                        "value": {"status": "done", "result": result}
                    }

                    self._publish_up(json.dumps(job_response))

            elif method.startswith('#status'):
                self._handle_delta_status(payload['value'])

            elif method.startswith('#now'):
                self._time_callback(self, payload['value'])

            else:
                logger.info("[{}] job {} not supported ".format(
                    self.id, method))

                job_response = {
                    "key": "@" + method,
                    "value": {"status": "failed", "message": "method not supported"}
                }

                self._publish_up(json.dumps(job_response))

        except Exception as e:
            logger.error("Error", e)

    def _build_ingestion_topic(self, tag):
        # build the topic for the ingestion
        # ex.  data/<deviceid>/<TAG>/
        return '/'.join([self.data_topic, tag])

    def send_event(self, value):
        """
    .. method:: send_event(tag, value)

       Publish an event to the ZDM.

       * :samp:`value`, the value of the event as dictionary.
       """
        self._send_up_msg('', 'event', value)

    def create_condition(self, tag, payload=None):
        condition = Condition(self, tag, payload)
        return condition

    def _open_condition(self, uuid, tag, start, payload=None):
        value = {
            'uuid': uuid,
            'tag': tag,
            'payload': payload,
            'start': start
        }
        self._send_up_msg('', 'condition', value)

    def _close_condition(self, uuid, finish):
        value = {
            'uuid': uuid,
            'finish': finish
        }
        self._send_up_msg('', 'condition', value)

    def _send_up_msg(self, prefix, key, value):
        msg = {
            'key': prefix + key,
            'value': value
        }
        self.mqttClient.publish(self.up_topic, msg)


class Condition:
    def __init__(self, client, tag, payload=None):
        self.uuid = str(time.time() * 1000.0)
        self.tag = tag
        self.payload = payload
        self.client = client

        self.start = None
        self.finish = None

    def open(self, start=None):
        if start is None:
            d = datetime.datetime.utcnow()
            self.start = d.isoformat("T") + "Z"
        else:
            self.start = start

        self.client._open_condition(self.uuid, self.tag, self.start, self.payload)

    def close(self, finish=None):
        if finish is None:
            d = datetime.datetime.utcnow()
            self.finish = d.isoformat("T") + "Z"
        else:
            self.finish = finish

        self.client._close_condition(self.uuid, self.finish)

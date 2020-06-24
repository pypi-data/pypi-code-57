"""
Engine that recieves salt commands from Odoo bus.
"""
from __future__ import absolute_import, print_function, unicode_literals
import concurrent.futures
from functools import partial
from httpclient_session import Session
import logging
import os
import salt.utils.event
from salt.utils import json
import salt.utils.process
from salt.ext.tornado.locks import Event
from salt.ext.tornado import ioloop
from salt.ext.tornado.web import Application
from salt.ext.tornado.httpserver import HTTPServer
from salt.ext.tornado.httpclient import AsyncHTTPClient, HTTPRequest
from salt.ext.tornado.web import RequestHandler
from salt.ext.tornado.gen import sleep, coroutine
import sys
import time
import uuid


log = logging.getLogger(__name__)

__virtualname__ = 'odoo_connector'

CHANNEL_PREFIX = 'remote_agent'


def __virtual__():
    return __virtualname__


def start(**kwargs):
    log.info('Starting Odoo bus engine...')
    OdooConnector(**kwargs).start()


class OdooConnector:
    db_selected = False
    http_session = None  # Requests session for bus polling
    db_selected = False    
    # Init token
    token = old_token = None
    token_update_time = time.time()
    # Default timeout
    bus_timeout = 60
    refresh_token_seconds = 300
    # Update on start before making first ping.
    token_updated = Event()

    def __init__(self, http_listen_address='0.0.0.0',
                 http_listen_port=30000,
                 http_enabled=False, bus_enabled=True):
        self.http_listen_port = http_listen_port
        self.http_listen_address = http_listen_address
        self.http_enabled = http_enabled
        self.bus_enabled = bus_enabled

    def start(self):
        # Set some options
        salt.utils.process.appendproctitle(self.__class__.__name__)
        self.bus_timeout = int(
            __salt__['config.get']('odoo_bus_timeout', 60))
        self.refresh_token_seconds = float(__salt__['config.get'](
            'odoo_refresh_token_seconds', 300))
        # Start workers
        self.io_loop = ioloop.IOLoop(make_current=False)
        self.io_loop.make_current()
        self.io_loop.spawn_callback(self.poll_bus)
        self.io_loop.spawn_callback(self.update_token)
        self.io_loop.spawn_callback(self.listen_http)
        self.http_session = Session()
        self.io_loop.start()

    async def select_db(self):
        """
        For multi database Odoo setup it is required to first select a database
        to work with. But if you have single db setup or use db_filters
        so that always one db is selected set odoo_single_db=True in settings.
        """
        if self.db_selected:
            return
        log.debug('Selecting Odoo database (session refresh)')
        scheme = 'https' if __salt__['config.get']('odoo_use_ssl') else 'http'
        auth_url = '{}://{}:{}/web/session/authenticate'.format(
            scheme, __salt__['config.get']('odoo_host', 'localhost'),
            int(__salt__['config.get']('odoo_bus_port', 8072)))
        log.debug('Odoo authenticate at %s', auth_url)
        data = {
            'jsonrpc': '2.0',
            'params': {
                'context': {},
                'db': __salt__['config.get']('odoo_db', 'demo'),
                'login': __salt__['config.get']('odoo_user', 'admin'),
                'password': __salt__['config.get']('odoo_password'),
            },
        }
        headers = {
            'Content-type': 'application/json'
        }
        req = HTTPRequest(auth_url, method='POST', body=json.dumps(data),
                          headers=headers)
        rep = await self.http_session.fetch(req)
        result = json.loads(rep.body)
        if rep.code != 200 or result.get('error'):
            log.error(u'Odoo authenticate error {}: {}'.format(
                rep.code,
                json.dumps(result['error'], indent=2)))
        else:
            log.info('Odoo authenticated for long polling.')
        self.db_selected = True

    def send_ping(self):
        __salt__['odoo.execute']('bus.bus', 'sendone', 
                 ['remote_agent/{}'.format(__grains__['id']),
                  {'command': 'ping'}])

    async def poll_bus(self):
        """
        Odoo bus poller to get massages from Odoo
        and convert it in Salt job.
        """
        # Wait for the new token.
        if not self.bus_enabled:
            log.debug('Odoo bus not enabled.')
            return
        await self.token_updated.wait()
        # Send the first ping message that will be omitted.
        self.send_ping()
        # Init the message pointer.
        last = 0
        scheme = 'https' if __salt__['config.get']('odoo_use_ssl') else 'http'
        while True:
            try:
                bus_url = '{}://{}:{}/longpolling/poll'.format(
                    scheme,
                    __salt__['config.get']('odoo_host', 'localhost'),
                    int(__salt__['config.get']('odoo_bus_port', 8072))
                )
                # Select DB first
                if not __salt__['config.get']('odoo_single_db'):
                    await self.select_db()
                # Now let try to poll
                log.debug('Polling %s.', bus_url)
                req = HTTPRequest(
                    bus_url,
                    method='POST',
                    body=json.dumps({'params': {
                        'last': last,
                        'channels': ['{}/{}'.format(
                            CHANNEL_PREFIX, __grains__['id'])]}}),
                    headers={'Content-Type': 'application/json'},
                    request_timeout=self.bus_timeout)
                r = await self.http_session.fetch(req)
                try:
                    json.loads(r.body)
                except ValueError:
                    log.error('JSON parse bus reply error: %s', r.body)
                result = json.loads(r.body).get('result')
                if not result:
                    error = json.loads(r.body).get(
                        'error', {}).get('data', {}).get('message')
                    if error:
                        log.error('Odoo bus error: %s', error)
                        # Sleep 1 sec not to flood the log.
                        await sleep(1)
                        continue
                if last == 0:
                    # Ommit queued data
                    for msg in result:
                        log.debug('Ommit bus message %s', str(msg)[:512])
                        last = msg['id']
                    continue
                # TODO: Check that tis is really
                # my channel as Odoo can send a match
                for msg in result:
                    last = msg['id']
                    log.debug('Received bus message %s', str(msg)[:512])
                    try:
                        f = partial(
                            self.handle_message_async,
                            msg['channel'], msg['message'])
                        self.io_loop.spawn_callback(f)
                    except Exception:
                        log.exception('Handle bus message error:')

            except Exception as e:
                no_wait = False
                if 'Connection refused' in str(e):
                    log.warning('Odoo Connection refused.')
                elif 'Stream closed' in str(e):
                    log.warning('Odoo Connection closed.')
                elif 'Timeout' in str(e):
                    # Do not wait on reconnect on notmal timeouts.
                    no_wait = True
                    log.info('Bus poll timeout, re-polling.')
                else:
                    log.exception('Bus error:')
                if not no_wait:
                    await sleep(1)

    async def handle_message_async(self, channel, message):
        @coroutine
        def blocking_call():
            f = partial(self.handle_message, channel, message)
            future = executor.submit(f)
            return (yield future)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        await blocking_call()

    def handle_message(self, channel, raw_message):
        # Check message type
        try:
            message = raw_message if isinstance(
                raw_message, dict) else json.loads(raw_message)
        except TypeError:
            log.error('Cannot load json from message: %s', raw_message)
            return
        # Check for security token
        if not self.check_security_token(message.get('token')):
            return
        # Check if this is known commands.
        if message.get('command') not in ['nameko_rpc', 'ping', 'restart']:
            log.error('Uknown command: %s', message)
            return
        # Restart
        if message.get('command') == 'restart':            
            log.info('Restart command received. Restarting')
            # Overwrite the last command not to get it again.
            self.send_ping()
            # Notify user
            uid = message.get('notify_uid')
            if uid:
                try:
                    __salt__['odoo.notify_user'](uid, 'Restarting...')
                except Exception:
                    log.exception('Restart notify error.')
            # Reply the command
            __salt__['odoo.execute'](
                'bus.bus', 'sendone',
                [message.get('reply_channel'), {'status': 'ok'}])
            # Restart
            __salt__['cmd.run']('systemctl restart odoopbx-agent')
        # Ping
        if message.get('command') == 'ping':
            log.info('Odoo ping received.')
            uid = message.get('notify_uid')
            if uid:
                try:
                    __salt__['odoo.notify_user'](uid, 'Ping reply')
                except Exception:
                    log.exception('Ping reply error:')
            # Check if we need to confirm receive.
            if message.get('reply_channel'):
                __salt__['odoo.execute'](
                    'bus.bus', 'sendone',
                    [message.get('reply_channel'), {'status': 'ok'}])
            return
        result = {}
        if message.get('pass_back'):
            result['pass_back'] = message['pass_back']
        service = message.get('service')
        method = message.get('method')
        args = message.get('args', ())
        kwargs = message.get('kwargs', {})
        callback_model = message.get('callback_model')
        callback_method = message.get('callback_method')
        try:
            if service == '{}_ami'.format(__grains__['id']):
                # AMI command.
                result['result'] = __salt__[
                    'asterisk.call_ami_action'](args[0])
            elif service == '{}_files'.format(__grains__['id']):
                # Files command
                result['result'] = __salt__['asterisk.{}'.format(method)](
                    *args, **kwargs)
            elif service == '{}_security'.format(__grains__['id']):
                # Security command
                result['result'] = __salt__['asterisk.{}'.format(method)](
                    *args, **kwargs)
            else:
                log.error('Uknown service: %s', message)
                result.setdefault(
                    'error', {})['message'] = 'Unknown service'
        except Exception as e:
            result.setdefault(
                'error', {})['message'] = str(e)
        # Do we have callback targets?
        if callback_model and callback_method:
            log.debug('Execute %s.%s.', callback_model, callback_method)
            __salt__['odoo.execute'](callback_model, callback_method, [result])
        # Do we have to notify?
        if message.get('status_notify_uid'):
            uid = message['status_notify_uid']
            log.debug('Status notify to %s.', uid)
            error = result.get('error', {}).get('message')
            title = method.replace('_', ' ').capitalize()
            status = error if error else 'Success'
            __salt__['odoo.execute'](
                'bus.bus', 'sendone',
                ['remote_agent_notification_{}'.format(uid),
                 {'message': status,
                  'title': title,
                  'warning': bool(error)}])

    def check_security_token(self, token):
        if self.token == token:
            return True
        elif self.token != token:
            # Check for race condition when token has been just updated
            if self.old_token == token:
                if abs(time.time() - self.token_update_time) > 3:
                    log.error('Outdated token, ignoring message: %s', token)
                    return False
                else:
                    log.info('Accepting old token message: %s', token)
                    return True
            else:
                log.error('Bad message token: %s', token)
                return False

    async def update_token(self):
        log.debug('Odoo bus token updater started every %s seconds.',
                  self.refresh_token_seconds)
        while True:
            try:                
                new_token = uuid.uuid4().hex
                __pillar__['odoo_token'] = new_token
                if not __salt__.get('odoo.execute'):
                    log.error("__salt__['odoo.execute'] is not available!")
                    await sleep(self.refresh_token_seconds)
                    continue
                __salt__['odoo.execute'](
                    'remote_agent.agent', 'update_token', [new_token])
                log.debug('Odoo token updated.')
                if not self.token_updated.is_set():
                    self.token_updated.set()
                # Keep previous token
                self.old_token = self.token
                # Generate new token
                self.token = new_token
                # Keep time of token update
                self.token_update_time = time.time()
            except Exception:
                log.exception('Update token error:')
                # Prevent flood
                await sleep(1)
            finally:
                await sleep(self.refresh_token_seconds)

    async def listen_http(self):
        parent = self

        class WebHook(RequestHandler):
            # Copied from Salt engines webhook.
            async def post(self, tag):
                body = self.request.body
                headers = self.request.headers if isinstance(
                    self.request.headers, dict) else dict(self.request.headers)
                json_body = json.loads(body)
                json_body['token'] = headers.get('X-Token')
                await parent.handle_message_async(tag, json_body)

        # Is it enabled?
        if not (self.http_enabled and self.http_listen_port
                and self.http_listen_address):
            log.debug('Incoming Odoo HTTP listener is not enabled.')
            return
        log.info('Odoo incoming HTTP ready at %s:%s',
                 self.http_listen_address, self.http_listen_port)
        application = Application([(r"/(.*)", WebHook)])
        ssl_options = None
        #if all([ssl_crt, ssl_key]):
        #    ssl_options = {"certfile": ssl_crt, "keyfile": ssl_key}
        http_server = HTTPServer(application, ssl_options=ssl_options)
        http_server.listen(self.http_listen_port,
                           address=self.http_listen_address)

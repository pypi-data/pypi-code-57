"""
Engine that recieves salt commands from Odoo bus.
"""
from __future__ import absolute_import, print_function, unicode_literals
import salt.utils.event
from salt.utils import json
import logging
import requests
import salt.ext.tornado.ioloop
import threading
from time import sleep
import time
import uuid

log = logging.getLogger(__name__)

__virtualname__ = 'odoo_bus'

CHANNEL_PREFIX = 'remote_agent'


def __virtual__():
    if __salt__['config.get']('odoo_bus_enabled'):
        return True
    else:
        return False, 'Odoo bus engine is not enabled.'


def start():
    log.info('Starting Odoo bus engine...')
    OdooBus().start()


class OdooBus:
    db_selected = False
    http_session = None  # Requests session for bus polling
    db_selected = False
    http_session = requests.Session()
    # Init token
    token = old_token = None
    token_update_time = time.time()
    # Default timeout
    bus_timeout = 60
    refresh_token_seconds = 300
    # Update on start before making first ping.
    token_updated = threading.Event()

    def start(self):
        # Set some options
        self.bus_timeout = int(
            __salt__['config.get']('odoo_bus_timeout', 60))
        self.refresh_token_seconds = float(__salt__['config.get'](
            'odoo_refresh_token_seconds', 300))
        # Start workers
        threading.Thread(target=self.update_token).start()
        self.token_updated.wait()
        self.poll_bus()

    def select_db(self):
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
        rep = self.http_session.post(
            auth_url,
            verify=__salt__['config.get']('odoo_verify_ssl', False),
            data=json.dumps(data),
            headers=headers)
        result = rep.json()
        if rep.status_code != 200 or result.get('error'):
            log.error(u'Odoo authenticate error {}: {}'.format(
                rep.status_code,
                json.dumps(result['error'], indent=2)))
        else:
            log.info('Odoo authenticated for long polling.')
        self.db_selected = True

    def poll_bus(self):
        """
        Odoo bus poller to get massages from Odoo
        and convert it in Salt job.
        """
        # Send the first ping message that will be omitted.
        __salt__['odoo.execute']('bus.bus', 'sendone', 
                 ['remote_agent/{}'.format(__grains__['id']),
                  {'command': 'ping'}])
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
                    self.select_db()
                # Now let try to poll
                log.debug('Polling %s.', bus_url)
                r = self.http_session.post(
                    bus_url,
                    timeout=self.bus_timeout,
                    verify=__salt__['config.get']('odoo_verify_ssl', False),
                    headers={'Content-Type': 'application/json'},
                    json={
                        'params': {
                            'last': last,
                            'channels': ['{}/{}'.format(
                                CHANNEL_PREFIX, __grains__['id'])]}})
                try:
                    r.json()
                except ValueError:
                    log.error('JSON parse bus reply error: %s', r.text)
                result = r.json().get('result')
                if not result:
                    error = r.json().get(
                        'error', {}).get('data', {}).get('message')
                    if error:
                        log.error('Odoo bus error: %s', error)
                        # Sleep 1 sec not to flood the log.
                        sleep(1)
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
                        self.handle_bus_message(msg['channel'], msg['message'])
                    except Exception:
                        log.exception('Handle bus message error:')

            except Exception as e:
                no_wait = False
                if isinstance(e, requests.exceptions.ConnectionError):
                    if 'Connection aborted' in str(e):
                        log.warning('Odoo Connection aborted')
                    elif 'Failed to establish' in str(e):
                        log.warning('Odoo Connection refused')
                    else:
                        log.warning(e.strerror)
                elif isinstance(e, requests.exceptions.HTTPError):
                    log.warning(r.reason)
                elif isinstance(e, requests.exceptions.ReadTimeout):
                    # Do not wait on reconnect on notmal timeouts.
                    no_wait = True
                    log.info('Bus poll timeout, re-polling')
                else:
                    log.exception('Bus error:')
                if not no_wait:
                    sleep(1)

    def handle_bus_message(self, channel, raw_message):
        # Check message type
        try:
            message = json.loads(raw_message)
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
        result = {}
        if message.get('pass_back'):
            result['pass_back'] = message['pass_back']
        service = message['service']
        method = message['method']
        args = message.get('args', ())
        kwargs = message.get('kwargs', {})
        callback_model = message.get('callback_model')
        callback_method = message.get('callback_method')
        try:
            if service == '{}_ami'.format(__grains__['id']):
                # AMI command.
                # TODO: Direct connection to Asterisk and send back result
                result['result'] = __salt__['event.fire'](args[0], 'ami_action')
            elif service == '{}_files'.format(__grains__['id']):
                result['result'] = __salt__['asterisk.{}'.format(method)](
                    *args, **kwargs)
            elif service == '{}_security'.format(__grains__['id']):
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

    def update_token(self):
        log.debug('Odoo bus token updater started every %s seconds.',
                  self.refresh_token_seconds)
        while True:
            try:                
                new_token = uuid.uuid4().hex
                if not __salt__.get('odoo.execute'):
                    log.error("__salt__['odoo.execute'] is not available!")
                    sleep(self.refresh_token_seconds)
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
                sleep(1)
            finally:
                sleep(self.refresh_token_seconds)

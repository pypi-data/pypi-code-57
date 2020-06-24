import logging
from salt.utils import json
import time

__virtualname__ = 'odoo'

# Import third party libs
try:
    import odoorpc
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

log = logging.getLogger(__name__)


def __virtual__():
    '''
    Only load if celery libraries exist.
    '''
    if not HAS_LIBS:
        return False, 'Odoo-RPC lib not found, odoo module not available.'
    # Return virtual module name:
    return 'odoo'


def ping():
    return 'pong'


def _get_odoo(host=None, port=None, user=None, password=None, db=None,
              protocol=None):
    """
    This is helper function to login into Odoo and share the connection.
    """
    odoo = __context__.get('odoo_client')
    if not odoo:
        # Set connection options.
        if not host:
            host = __salt__['config.get']('odoo_host', 'localhost')
        if not port:
            port = int(__salt__['config.get']('odoo_port', 8069))
        if not db:
            db = __salt__['config.get']('odoo_db', 'demo')
        if not user:
            user = __salt__['config.get']('odoo_user', 'admin')
        if not password:
            password = __salt__['config.get']('odoo_password', 'admin')
        if not protocol:
            protocol = 'jsonrpc+ssl' if __salt__['config.get'](
                'odoo_use_ssl') else 'jsonrpc'
        # Create an OdooRPC object and login.
        try:
            odoo = odoorpc.ODOO(host, port=port, protocol=protocol)
            odoo.login(db, user, password)
            # Keep the connection object in salt context.
            __context__['odoo_client'] = odoo
        except Exception as e:
            log.error('Odoo connection error: %s', e)
    return odoo


def execute(model, method, args, kwargs={}):
    """
    Execute Odoo method.

    CLI example: odoo.execute res.partner search '[[["name","ilike","admin"]]]'
    """
    log.debug('Odoo execute: %s.%s %s %s', model, method, args, kwargs)
    odoo = _get_odoo()
    if not odoo:
        log.error('Odoo not connected.')
        return
    # Try to parse args
    if type(args) is str:
        args = json.loads(args)
    args = tuple(args)
    res = getattr(odoo.env[model], method)(*args, **kwargs)
    return res


def send_ami_event(event):
    """
    Send AMI event to Odoo according to events map.
    """
    event_name = event.get('Event')
    # Iterate over Asterisk events and select only current event handlers.
    handlers = [k for k in (__pillar__.get('asterisk_events_map') or []) if k[
                'name'] == event_name and k['source'] == 'AMI']
    for handler in handlers:
        # Check for event condition
        if handler.get('condition'):
            # Handler has a condition so evaluate it first.
            try:
                # TODO: Create a more secure eval context.
                res = eval(handler['condition'],
                           None, {'event': event})
                if not res:
                    # The confition evaluated to False so do not send.
                    continue
            except Exception:
                log.exception(
                    'Error evaluating condition: %s, event: %s',
                    handler['condition'], event)
                # The confition evaluated to error so do not send.
                continue
        # Sometimes it's required to send event to Odoo with a delay.
        if handler.get('delay'):
            time.sleep(int(handler['delay']))
        # Finally send event to Odoo.
        odoo = _get_odoo()
        getattr(
            odoo.env[handler['model']], handler['method'])(event)
        log.debug('Event %s has been sent to Odoo', event_name)


def notify_user(uid, message, title='Notification',
                warning=False, sticky=False):
    """
    Send notification to Odoo user by his uid.

    CLI examples:
        salt asterisk odoo.notify_user 2 'Hello admin!'
        salt asterisk odoo.notify_user 2 'Error' warning=True sticky=True
    """    
    log.debug('Notify user %s: %s', uid, message)
    odoo = _get_odoo()
    __salt__['odoo.execute'](
        'bus.bus', 'sendone',
        ['remote_agent_notification_{}'.format(uid), {
            'message': message,
            'warning': warning,
            'sticky': sticky,
            'title': title
        }])

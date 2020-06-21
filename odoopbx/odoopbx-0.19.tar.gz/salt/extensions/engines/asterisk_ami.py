'''
This is Asterisk PBX Salt module
'''
from __future__ import absolute_import, print_function, unicode_literals
import asyncio
from aiorun import run
import logging
import salt.utils.event
from salt.utils import json
try:
    from panoramisk import Manager
    from panoramisk.message import Message as AsteriskMessage
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

__virtualname__ = 'asterisk_ami'

log = logging.getLogger(__name__)


def __virtual__():
    if not HAS_LIBS:
        return False, 'Panoramisk lib not found, asterisk module not available.'
    return True


class AmiClient:

    async def start(self):
        manager_disconnected = asyncio.Event()
        self.loop = asyncio.get_event_loop()
        # Create event loop to receive actions as events.
        self.loop.create_task(self.action_event_loop())
        self.manager = Manager(
            loop=self.loop,
            forgetable_actions=('ping', 'login', 'command'),
            host=__salt__['config.get']('ami_host', 'localhost'),
            port=int(__salt__['config.get']('ami_port', '5038')),
            username=__salt__['config.get']('ami_login', 'salt'),
            secret=__salt__['config.get']('ami_secret', 'stack')
        )
        # Register events
        for ev_name in __salt__['config.get']('ami_register_events', []):
            log.info('Registering for AMI event %s', ev_name)
            self.manager.register_event(ev_name, self.on_asterisk_event)
        
        try:
            await self.manager.connect()
            log.info('Connected to AMI.')
        except Exception as e:
            log.error('Cannot connect to Asterisk AMI: %s', e)
        await manager_disconnected.wait()

    async def on_asterisk_event(self, manager, event):
        event = dict(event)
        trace_events = __opts__.get('ami_trace_events')
        if trace_events:
            if isinstance(trace_events, bool):
                log.info('AMI event: %s', json.dumps(event, indent=2))
            elif isinstance(
                    trace_events, list) and event['Event'] in trace_events:
                log.info('AMI event: %s', json.dumps(event, indent=2))
        __salt__['event.fire'](event, 'AMI/{}'.format(event['Event']))

    async def action_event_loop(self):
        log.debug('AMI action_event_loop started.')
        event = salt.utils.event.MinionEvent(__opts__)
        while True:
            try:
                evdata = event.get_event(tag='ami_action',
                                         no_block=True)
                # TODO: Connect to Salt's tornado eventloop.
                await asyncio.sleep(0.01)
                if evdata:
                    reply_channel = evdata.pop('reply_channel', False)
                    res = await self.manager.send_action(evdata)
                    if not isinstance(res, list):
                        res = [res]
                    if reply_channel:
                        # Send back the result.
                        __salt__['event.fire'](
                            {'Reply': [dict(k) for k in res]},
                            'ami_reply/{}'.format(reply_channel))
                    trace_actions = __opts__.get('ami_trace_actions')
                    if trace_actions and isinstance(trace_actions, bool):
                        log.info('Action request: %s', evdata)
                        log.info('Action result: %s', res)
                    elif isinstance(trace_actions, list) and evdata[
                            'Action'] in trace_actions:
                        log.info('Action request: %s', evdata)
                        log.info('Action result: %s', res)

            except Exception:
                log.exception('AMI action event loop error:')
                await asyncio.sleep(1)  # Protect log flood.


def start():
    log.info('Starting Asterisk AMI engine.')
    run(AmiClient().start())

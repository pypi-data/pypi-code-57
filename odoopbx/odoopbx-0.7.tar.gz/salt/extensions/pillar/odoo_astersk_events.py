'''
Pillar that takes events map from Odoo
'''
import logging

log = logging.getLogger(__name__)

try:
    import odoorpc
    HAVE_LIBS = True
except ImportError:
    HAVE_LIBS = False

__virtualname__ = 'odoo_asterisk_events'

def __virtual__():
    if HAVE_LIBS:
        return True
    return False    

def ext_pillar(minion_id, pillar, config):
    try:
        events_map = __salt__['odoo.execute'](
            'asterisk_common.event', 'search_read', [
                [['is_enabled', '=', True], ['source', '=', 'AMI']]])
        return {
            'asterisk_events_map': events_map
        }
    except Exception as e:
        log.info('Events map not loaded: %s', e)
        return {
            # Do not return events            
            'asterisk_events_map': []
        }

from zuper_commons.types import ZException
from zuper_typing import can_be_used_as2
from .language import InteractionProtocol

__all__ = ['IncompatibleProtocol', 'check_compatible_protocol']


class IncompatibleProtocol(ZException):
    pass


def check_compatible_protocol(p1: InteractionProtocol, p2: InteractionProtocol):
    """ Checks that p1 is a subprotocol of p2 """
    try:
        # check input compatibility
        # we should have all inputs
        for k, v2 in p2.inputs.items():

            if not k in p1.inputs:
                msg = f'First protocol misses input "{k}".'
                raise IncompatibleProtocol(msg)
            v1 = p1.inputs[k]
            r = can_be_used_as2(v1, v2)
            if not r:
                msg = f'For input "{k}", cannot use type {v1} as {v2}: {r}'
                raise IncompatibleProtocol(msg)

        # check output compatibility
        # we should have all inputs
        for k, v2 in p2.outputs.items():
            if not k in p1.outputs:
                msg = f'First protocol misses output "{k}".'
                raise IncompatibleProtocol(msg)
            v1 = p1.outputs[k]
            r = can_be_used_as2(v1, v2)
            if not r:
                msg = f'For output "{k}", cannot use type {v1} as {v2}: {r}'
                raise IncompatibleProtocol(msg)
            # XXX: to finish
    except IncompatibleProtocol as e:
        msg = "Cannot say that p1 is a sub-protocol of p2"
        raise IncompatibleProtocol(msg, p1=p1, p2=p2) from e

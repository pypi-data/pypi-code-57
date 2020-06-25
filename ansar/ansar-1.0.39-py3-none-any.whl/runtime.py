# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017, 2018, 2019, 2020 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module contains the status and control information associated
with the execution of Ansar code. There is an object that holds flags
dictating what logging is generated during sending of a :py:mod:`~ansar.message`
and there are the constants that appear in those objects.

.. autoclass:: Runtime
"""
__docformat__ = 'restructuredtext'


__all__ = [
    'USER_LOG_FAULT',
    'USER_LOG_WARNING',
    'USER_LOG_CONSOLE',
    'USER_LOG_TRACE',
    'USER_LOG_DEBUG',
    'USER_LOG_NONE',

    'TAG_ANSAR',

    'TAG_CREATED',
    'TAG_DESTROYED',
    'TAG_SENT',
    'TAG_RECEIVED',
    'TAG_TRACKING',
    'TAG_FAULT',
    'TAG_WARNING',
    'TAG_CONSOLE',
    'TAG_TRACE',
    'TAG_DEBUG',

    'ANSAR_CREATED',
    'ANSAR_DESTROYED',
    'ANSAR_SENT',
    'ANSAR_RECEIVED',
    'ANSAR_TRACKING',
    'ANSAR_FAULT',
    'ANSAR_WARNING',
    'ANSAR_CONSOLE',
    'ANSAR_TRACE',
    'ANSAR_DEBUG',

    'Runtime',
    'CodingProblem',
    'PlatformFailure',
]

#
#

#
#
USER_LOG_NONE = 100     # No user logs at all.
USER_LOG_FAULT = 6      # A definite problem that will compromise the service.
USER_LOG_WARNING = 5    # Something unexpected that may compromise the service.
USER_LOG_TRACKING = 4
USER_LOG_CONSOLE = 3    # An operational milestone worthy of note.
USER_LOG_TRACE = 2      # Progress of the service. Suitable for public viewing.
USER_LOG_DEBUG = 1      # Not suitable for customer or support.

TAG_ANSAR = 'A'

TAG_CREATED   = '+'
TAG_DESTROYED = 'X'
TAG_SENT      = '>'
TAG_RECEIVED  = '<'
TAG_TRACKING  = '~'
TAG_FAULT     = '!'
TAG_WARNING   = '?'
TAG_CONSOLE   = '^'
TAG_TRACE     = 'T'
TAG_DEBUG     = '_'

ANSAR_CREATED   = TAG_ANSAR + TAG_CREATED
ANSAR_DESTROYED = TAG_ANSAR + TAG_DESTROYED
ANSAR_SENT      = TAG_ANSAR + TAG_SENT
ANSAR_RECEIVED  = TAG_ANSAR + TAG_RECEIVED
ANSAR_TRACKING  = TAG_ANSAR + TAG_TRACKING
ANSAR_FAULT     = TAG_ANSAR + TAG_FAULT
ANSAR_WARNING   = TAG_ANSAR + TAG_WARNING
ANSAR_CONSOLE   = TAG_ANSAR + TAG_CONSOLE
ANSAR_TRACE     = TAG_ANSAR + TAG_TRACE
ANSAR_DEBUG     = TAG_ANSAR + TAG_DEBUG

#
#
class Runtime(object):
    def __init__(self,
        name,
        module,
        value,
        version_history,
        lifecycle=True, message_trail=True,
        execution_trace=True,
        copy_before_sending=True,
        not_portable=False,
        user_logs=USER_LOG_CONSOLE):
        self.name = name        # Last component of dotted name.
        self.module = module    # Full path up to the name.
        self.version_history = version_history
        self.value = value      # Value of this binding, e.g. pointer to a function

        self.path = '%s.%s' % (module, name)

        self.lifecycle = lifecycle              # Create, destroy objects
        self.message_trail = message_trail      # Sending
        self.execution_trace = execution_trace  # Receiving
        self.copy_before_sending=copy_before_sending
        self.not_portable=not_portable
        self.user_logs = user_logs              # Object trace, warning...

#
#
class CodingProblem(Exception):
    """
    Exception thrown if there appears to have been a poor
    construction of an async entity.
    """
    def __init__(self, identify_and_help):
        Exception.__init__(self, identify_and_help)

#
#
class PlatformFailure(Exception):
    """
    Exception thrown if it appears that the underlying
    platform is not meeting its end of the deal.
    """
    def __init__(self, identify_and_help):
        Exception.__init__(self, identify_and_help)

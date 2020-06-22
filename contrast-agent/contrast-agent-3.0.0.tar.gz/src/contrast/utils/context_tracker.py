# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
from contextlib import contextmanager
from collections import defaultdict


class ContextTracker(object):
    CURRENT_CONTEXT = "CURRENT_CONTEXT"
    PARENT_ATTR = "cs__parent_id"

    def __init__(self):
        self._tracker = defaultdict(dict)

    def get(self, key, default=None):
        try:
            return self._tracker[self.current_thread_id()][key]
        except KeyError:
            return default

    def clear(self):
        self._tracker.clear()

    def get_explicit_context(self, thread_id, key, default=None):
        """"
        Can be used to retrieve a context from any thread, used when the current thread doesn't have a context
        but its 'parent' thread does
        """
        try:
            return self._tracker[thread_id][key]
        except KeyError:
            return default

    def set(self, key, value):
        self._tracker[self.current_thread_id()][key] = value

    def delete(self, key):
        current_thread_id = self.current_thread_id()

        if current_thread_id not in self._tracker:
            return

        del self._tracker[current_thread_id][key]

        if len(self._tracker[current_thread_id]) == 0:
            del self._tracker[current_thread_id]

    def set_current(self, value):
        self.set(self.CURRENT_CONTEXT, value)

    def delete_current(self):
        self.delete(self.CURRENT_CONTEXT)

    @contextmanager
    def lifespan(self, context):
        self.set_current(context)

        yield context

        self.delete_current()

    def current(self):
        context = self.get(self.CURRENT_CONTEXT)

        current_thread = threading.currentThread()

        if (
            context is None
            and hasattr(current_thread, self.PARENT_ATTR)
            and getattr(current_thread, self.PARENT_ATTR) in self._tracker
        ):
            return self.get_explicit_context(
                getattr(current_thread, self.PARENT_ATTR), self.CURRENT_CONTEXT
            )

        return context

    def current_thread_id(self):
        return threading.currentThread().ident

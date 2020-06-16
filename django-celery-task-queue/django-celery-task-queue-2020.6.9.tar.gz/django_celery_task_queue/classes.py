from datetime import datetime
import sys
from traceback import format_tb

from django.conf import settings
from django.db.utils import OperationalError
import requests

import django_celery_task_queue.signals as signals
from .models import Exc

class Task:
    model = None

    @classmethod
    def get_task_name(cls):
        return cls.model.get_task_name()

    @classmethod
    def as_func(cls):
        def func(*args,**kwargs):
            return cls().run(*args,**kwargs)
        return func

    def init(self):
        pass

    def process_task(self):
        pass

    def run(self,id,**kwargs):
        self.update_kwargs = {}
        self.id = id
        self.started_at = datetime.now()
        for k,v in kwargs.items():
            setattr(self,k,v)
        try:
            self.init()
            if self.id:
                self.process_task()
            if self.id:
                self.complete_task()
        except OperationalError as e:
            if 'deadlock' in str(e).lower(): # deadlock. shit happens
                self.restart_task()
                return
            self.save_exc()
            self.disable_task()
        except Exception:
            self.save_exc()
            self.disable_task()

    def delete_task(self):
        signals.task_deleted.send(sender=self.__class__, instance=self)
        self.model.objects.filter(id=self.id).delete()
        self.id = None

    def complete_task(self):
        if not self.id:
            return
        signals.task_completed.send(sender=self.__class__, instance=self)
        completed_at = datetime.now()
        self.update_kwargs.update(
            is_completed = True,
            is_enqueued = False,
            is_disabled = False,
            started_at = self.started_at,
            completed_at = completed_at
        )
        self.model.objects.filter(id=self.id).update(**self.update_kwargs)
        self.id = None

    def disable_task(self):
        signals.task_disabled.send(sender=self.__class__, instance=self)
        kwargs = dict(
            is_disabled = True,
            is_enqueued = False,
            enqueued_at = None,
            started_at = None,
            completed_at = None,
            disabled_at = datetime.now(),
        )
        self.model.objects.filter(id=self.id).update(**kwargs)
        self.id = None

    def restart_task(self):
        signals.task_restarted.send(sender=self.__class__, instance=self)
        self.model.objects.filter(id=self.id).update(
            is_completed = False,
            is_enqueued = False,
            is_disabled = False,
            enqueued_at = None,
            started_at = None,
            disabled_at = None
        )
        self.log_task(completed_at = None,is_restarted=True)
        self.id = None

    def save_exc(self):
        exc, exc_value, tb = sys.exc_info()
        Exc(
            db_table = self.model._meta.db_table,
            task_id = self.id,
            exc_type = exc.__module__+'.'+exc.__name__ if exc.__module__ else exc.__name__,
            exc_value = exc_value if exc_value else '',
            exc_traceback = '\n'.join(format_tb(tb))
        ).save()


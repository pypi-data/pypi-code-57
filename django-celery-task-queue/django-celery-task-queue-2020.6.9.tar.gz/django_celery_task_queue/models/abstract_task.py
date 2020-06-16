from datetime import datetime

from django.db import models


IGNORED_FIELDS = ['id','is_completed','is_enqueued','is_disabled','enqueued_at','disabled_at']

def getfields(model):
    return list(map(lambda f:f.name,
        filter(lambda f:f.name not in IGNORED_FIELDS,model._meta.fields),
    ))


class AbstractTask(models.Model):
    activated_at = models.DateTimeField(auto_now_add=True)
    enqueued_at = models.DateTimeField(null=True)
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
    disabled_at = models.DateTimeField(null=True)

    is_completed = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_enqueued = models.BooleanField(default=False)

    priority = models.IntegerField(default=0,null=False)

    task_name = None

    class Meta:
        abstract = True

    @classmethod
    def get_task_name(model):
        return model.task_name if model.task_name else model._meta.db_table

    @classmethod
    def send_tasks(model,app,enqueued_limit):
        count = enqueued_limit-model.objects.filter(is_enqueued=True).count()
        if count<=0:
            return
        qs = model.objects.filter(
            is_completed=False,is_enqueued=False,is_disabled=False
        ).only(*getfields(model)).order_by('-priority')
        ids = []
        task_messages = []
        enqueued_at = datetime.now()
        for r in qs[0:count]:
            ids.append(r.id)
            kwargs = dict(enqueued_at=enqueued_at)
            for f in getfields(model):
                kwargs[f] = getattr(r,f)
            task_messages.append(dict(args=[r.id],kwargs=kwargs))
        if ids:
            task_name = model.get_task_name()
            model.objects.filter(id__in=ids).update(is_enqueued=True,enqueued_at=enqueued_at)
            for task_msg in task_messages:
                app.send_task(task_name,args=task_msg['args'],kwargs=task_msg['kwargs'])


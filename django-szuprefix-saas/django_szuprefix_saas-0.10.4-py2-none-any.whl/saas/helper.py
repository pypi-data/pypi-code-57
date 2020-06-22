# -*- coding:utf-8 -*- 
__author__ = 'denishuang'
from django.conf import settings
from . import models

class ResourceRegister(object):
    def __init__(self):
        self.reg_map = {}

    def register(self, content_type, func):
        self.reg_map[content_type] = func

    def verify(self, content_type, user, ids):
        if content_type not in self.reg_map:
            raise KeyError(u'%s not registered yet.' % content_type)
        func = self.reg_map[content_type]
        return func(content_type, user, ids)


def initDepartmentAndManagerWorker(party):
    party.root_department
    party.master_worker

def get_default_party():
    return models.Party.objects.get(id=settings.DEFAULT_SAAS_PARTY)


def get_user_scope_map(user):
    roles = list(user.saas_roles.all())
    if not roles:
        return
    rsm = {}
    for r in roles:
        rsm.update(r.permissions)
    return rsm
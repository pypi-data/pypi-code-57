# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models, helper
from ..saas.models import Party


def do_dailylog_stat(the_date=None):
    from datetime import date
    the_date = the_date or date.today()
    print 'do_dailylog_stat', the_date
    for p in Party.objects.all():
        print p, helper.do_daily_stat(the_date, p)

def gen_dailylog_records(the_date=None):
    from datetime import date
    the_date = the_date or date.today()
    print 'gen_dailylog_records', the_date
    for p in Party.objects.all():
        print p, helper.gen_dailylog_records(the_date, p)

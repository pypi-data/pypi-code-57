# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType


def do_daily_stat(the_date, party):
    d = {}
    for l in party.dailylog_dailylogs.filter(the_date=the_date):
        for k, v in l.context.iteritems():
            ps = k.split('.')
            app, model, mid, category, metric = ps
            am = (app, model)
            mt = "%s.%s" % (category, metric)
            r = d.setdefault(am, {}).setdefault(mid, {}).setdefault(mt, {'v': 0, 'u': 0})
            r['u'] += 1
            r['v'] += v
            r2 = d.setdefault(am, {}).setdefault(None, {}).setdefault(mt, {'v': 0, 'u': 0, 'us': set()})
            r2['us'].add(l.user.id)
            r2['u'] = len(r2['us'])
            r2['v'] += v
    for am, dam in d.iteritems():
        ct = ContentType.objects.get_by_natural_key(am[0], am[1])
        for oid, doid in dam.iteritems():
            for mt, dmt in doid.iteritems():
                party.dailylog_stats.update_or_create(the_date=the_date, owner_type=ct, owner_id=oid, metics=mt,
                                                      defaults=dict(value=dmt['v'], user_count=dmt['u']))
    return d


def gen_dailylog_records(the_date, party):
    for l in party.dailylog_dailylogs.filter(the_date=the_date):
        for k, v in l.context.iteritems():
            ps = k.split('.')
            app, model, mid, category, metric = ps
            mt = "%s.%s" % (category, metric)
            ct = ContentType.objects.get_by_natural_key(app, model)
            party.dailylog_records.update_or_create(the_date=the_date, owner_type=ct, owner_id=mid, metics=mt, user=l.user,
                                                      defaults=dict(value=v))


def save_performance(d, user, party):
    ct = ContentType.objects.get(app_label=d['app'], model=d['model'])
    p, created = party.dailylog_performances.update_or_create(user=user, owner_type=ct, owner_id=d['owner_id'], defaults=dict(
        detail=d['detail']
    ))
    return p


def get_performance(d, user, party):
    ct = ContentType.objects.get(app_label=d['app'], model=d['model'])
    p, created = party.dailylog_performances.get_or_create(user=user, owner_type=ct, owner_id=d['owner_id'], defaults={})
    return p


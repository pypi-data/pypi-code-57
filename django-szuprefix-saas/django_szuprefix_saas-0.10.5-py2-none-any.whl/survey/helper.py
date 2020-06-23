# -*- coding:utf-8 -*- 
__author__ = 'denishuang'
import logging

from datetime import datetime, timedelta
from . import models

log = logging.getLogger("django")


def stat_survey_answers(survey):
    r = {}
    paper = survey.content_object
    qs = {}
    for g in paper['groups']:
        for q in g['questions']:
            qs[q['id']] = q
    for answer in survey.answers.all():
        als = answer.detail
        for a in als:
            qid = a['id']
            question = qs[qid]
            qtype = question['type']
            v = a['userAnswer']
            d = r.setdefault(qid, [{}] * len(v))
            for i in range(len(v)):
                vi = v[i]
                if qtype == 'multiple':
                    for a in vi:
                        d[i].setdefault(a, 0)
                        d[i][a] += 1
                else:
                    d[i].setdefault(vi, 0)
                    d[i][vi] += 1
    for qid, stat in r.iteritems():
        qs[qid]['stat'] = stat
    return survey


def create_survey_todos(survey):
    now = datetime.now()
    if survey.begin_time > now:
        log.warn('开始时间未到: %s ' % survey.begin_time)
        return
    if survey.end_time < now:
        log.warn('结束时间已过:%s' % survey.end_time)
        return
    uids = survey.get_not_answer_user_ids()
    from django_szuprefix_saas.todo.helper import create_todos
    create_todos(
        target=survey,
        name=survey.title,
        url="/survey/survey/%d/" % survey.id,
        user_ids=uids,
        expiration=survey.end_time
    )


def batch_create_survey_todos():
    now = datetime.now()
    outtime = now - timedelta(hours=1)
    for s in models.Survey.objects.filter(is_active=True, begin_time__lt=now, end_time__gt=now, begin_time__gt=outtime):
        create_survey_todos(s)

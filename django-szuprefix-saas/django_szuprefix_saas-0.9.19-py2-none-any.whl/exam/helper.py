# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

__author__ = 'denishuang'
import re
from django_szuprefix.utils.datautils import strQ2B
from . import models, choices


def distrib_count(d, a):
    a = str(a)
    counts = d.setdefault('counts', {})
    percents = d.setdefault('percents', {})
    counts[a] = counts.setdefault(a, 0) + 1
    tc = sum(counts.values())
    cas = [(int(float(k)), v) for k, v in counts.iteritems()]
    cas.sort()
    s = 0
    for k, v in cas:
        s += v
        percents[str(k)] = s / float(tc)
    d['count'] = tc
    return d


def answer_is_empty(a):
    if isinstance(a, (list, tuple)):
        return not any(a)
    return not a


def answer_equal(standard_answer, user_answer):
    if len(standard_answer) != len(user_answer):
        return False
    l = zip(standard_answer, user_answer)
    return all([b in a.split('|') for a, b in l])


RE_MULTI_ANSWER_SPLITER = re.compile(r"[|()、]")


def split_answers(s):
    if isinstance(s, (list, tuple)):
        return s
    return RE_MULTI_ANSWER_SPLITER.split(strQ2B(s))


"""
In [36]: answer_match(['A|C','B','C','D'],['C','B'],True)
Out[36]: 0.5

In [37]: answer_match(['A','B','C','D'],['C','B'])
Out[37]: 0.5

In [38]: answer_match(['A','B','C','D'],['B'])
Out[38]: 0.25

In [39]: answer_match(['A','B','C','D'],['B'],True)
Out[39]: 0.0

In [40]: answer_match(['A','B','C','D'],['B','E'])
Out[40]: 0.0

In [41]: answer_match(['A','B','C','D'],['B','A','D','C'])
Out[41]: 1.0
"""


def answer_match(standard_answer, user_answer, one_by_one=False):
    sa = standard_answer
    ua = user_answer
    lsa = len(sa)
    lua = len(ua)
    if lua > lsa:
        return -1
    l = zip(sa[:lua], ua)
    c = 0
    for s, u in l:
        if one_by_one:
            if u in split_answers(s):
                c += 1
        else:
            if u in sa:
                c += 1
            else:
                c = 0
                break
    return c / lsa


def extract_fault(answer):
    m = dict([(a['id'], a) for a in answer.detail if not (answer_is_empty(a['userAnswer']) or a['right'])])
    p = answer.paper.content_object
    rs = []
    for g in p['groups']:
        for q in g['questions']:
            qid = q['id']
            q['group'] = dict(title=g.get('title'), memo=g.get('memo'), number=g.get('number'))
            if qid in m:
                rs.append((q, m[qid]))
    return rs


def record_fault(answer):
    user = answer.user
    paper = answer.paper

    for question, qanswer in extract_fault(answer):
        question_id = question['id']
        lookup = dict(user=user, paper=paper, question_id=question_id)
        fault = models.Fault.objects.filter(**lookup).first()
        if not fault:
            models.Fault.objects.create(
                question=question,
                question_type=choices.MAP_QUESTION_TYPE.get(question['type']),
                detail=dict(lastAnswer=qanswer), **lookup
            )
        else:
            fault.times += 1
            fault.detail['last_answer'] = qanswer
            fault.corrected = False
            fault.question = question
            fault.is_active = True
            from datetime import datetime
            fault.create_time = datetime.now()
            rl = fault.detail.setdefault('result_list', [])
            rl.append(False)
            fault.save()


def cal_correct_straight_times(rl):
    c = 0
    for i in range(len(rl) - 1, -1, -1):
        if not rl[i]:
            break
        c += 1
    return c

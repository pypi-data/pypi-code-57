import json
import logging
import operator
import re
import sys
from collections import Counter
from dataclasses import asdict
from functools import reduce
from typing import Any, Iterable, List, Set, Tuple, Union

import click
import pandas as pd
from collections import namedtuple

# standard key in a JIRA issue
KEYS = ['assignee',
        'comment',
        'created',
        'creator',
        'description',
        'issuetype',
        'labels',
        'priority',
        'reporter',
        'status',
        'summary']

Issue = namedtuple('Issue', ['key']+KEYS)


Comment = namedtuple('Comment', ['author', 'updated', 'msg'])


def process_scalar(elt) -> str:
    return str(elt)


def process_list(elts: list) -> str:
    return ','.join(elts)


def process_name(elt: dict) -> str:
    return elt.get('name', '')


def process_comment(comments: list) -> Comment:
    return get_last_comment(comments)


def get_gist_comment(comment: dict, threshold: int) -> Comment:
    """retrieve key information

    cut-off description lenght at `threshold`

    """
    def normalize(text):
        if not text:
            return ''
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    text = comment['body']
    author = comment['author']
    author = author['displayName'] if 'displayName' in author else author['key']
    text = normalize(text) if len(
        text) < threshold else text[:threshold]+'[...]'
    return Comment(author, comment['updated'], text)


def get_last_comment(comments: list, threshold: int = 150) -> Comment:
    """sum up recent comment"""
    if len(comments) == 0:
        return Comment('', '', '')
    last_comment = comments[-1]
    return get_gist_comment(last_comment, threshold)


def comment2str(comment: Comment) -> str:
    if not comment.msg:
        return ''
    ts = comment.updated.split('T')[0]
    return f"{ts},{comment.author}:{comment.msg}"


def process_comments(comments):
    return get_last_comment(comments['comments'])


def get_gist_issue(key: str, issue: dict) -> Issue:
    def get_processor(k):
        fct = processor[k]
        try:
            return fct(issue[k])
        except Exception:
            return
    processor = {'assignee': process_name,
                 'comment': process_comments,
                 'created': process_scalar,
                 'creator': process_name,
                 'description': process_scalar,
                 'issuetype': process_name,
                 'labels': process_list,
                 'priority': process_name,
                 'reporter': process_name,
                 'status': process_name,
                 'summary': process_scalar}
    values = [key]+[get_processor(k) for k in KEYS]
    return Issue(*values)


def make_report(issues: list) -> pd.DataFrame:
    processed = [get_gist_issue(issue['key'], issue['fields'])
                 for issue in issues]
    df = pd.DataFrame(processed)
    df['comment'] = df['comment'].apply(comment2str)
    return df


@click.command()
@click.argument('reportfile', type=click.Path(dir_okay=True))
@click.argument('jsondata', type=click.File(mode='r'), default=sys.stdin)
def cli(reportfile, jsondata):
    # write a csv to reportfile
    issues = json.load(jsondata)['issues']
    click.echo(f'writing result to {reportfile}')
    make_report(issues).to_csv(reportfile, index=False)

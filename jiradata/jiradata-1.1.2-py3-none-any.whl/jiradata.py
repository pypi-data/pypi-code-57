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


def get_gist_issue(key: str, issue: dict, custom_field: dict = {}) -> dict:
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
    processor = {**processor, **custom_field}
    fields = {k: get_processor(k) for k in processor}
    fields['key'] = key
    return fields


def make_report(issues: list, custom:dict={}) -> pd.DataFrame:
    processed = [get_gist_issue(issue['key'], issue['fields'], custom)
                 for issue in issues]
    df = pd.DataFrame(processed)
    df['comment'] = df['comment'].apply(comment2str)
    return df


def add_epic(report: pd.DataFrame, epic_field: str) -> pd.DataFrame:
    epic = report.query('issuetype=="Epic"')[['key', 'description']]
    epic = epic.rename(
        columns={'description': 'epic_summary', 
                 'key': 'epic_key'})
    merged = pd.merge(left=report, right=epic, how='left',
                      left_on=epic_field, right_on='epic_key')
    return merged.drop(columns=epic_field)

def writecsv(df:pd.DataFrame,reportfile):
    df.sort_index(axis=1).to_csv(reportfile, index=False)

@click.command()
@click.argument('reportfile', type=click.Path(dir_okay=True))
@click.argument('jsondata', type=click.File(mode='r'), default=sys.stdin)
@click.option('--custom-field')
@click.option('--epic-field')
def cli(reportfile, jsondata, custom_field, epic_field):
    # write a csv to reportfile
    if custom_field:
        custom = {custom_field: lambda x: str(x)}
    elif epic_field:
        custom = {epic_field: lambda x:str(x)}
    else:
        custom = {}
    issues = json.load(jsondata)['issues']
    report = make_report(issues, custom=custom)
    if epic_field:
        click.echo(f'looking for epic using field {epic_field}')
        report = add_epic(report,epic_field)
        click.echo(f'writing result to {reportfile}')
        writecsv(report,reportfile)
    else:
        click.echo(f'writing result to {reportfile}')
        writecsv(report,reportfile)
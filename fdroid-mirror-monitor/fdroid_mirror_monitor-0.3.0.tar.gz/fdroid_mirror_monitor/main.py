#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor import repo, mirror, history, website
from fdroid_mirror_monitor.utils import get_logger, geoip, get_own_ip, get_mirrors_readme
# stdlibs
from datetime import datetime, timezone
from importlib.metadata import metadata
from os import makedirs, path
from queue import Queue
import argparse
import json
import threading
import traceback
import time


def main():
    parser = argparse.ArgumentParser(prog='fdroid_mirror_monitor', description=metadata(__package__)['Summary'])
    parser.add_argument('--no_history',
                        help='''don't create history.json''',
                        action='store_true')
    parser.add_argument('--no_html',
                        help='''don't create htmls''',
                        action='store_true')
    parser.add_argument('--html',
                        help='create htmls from status.json file')
    parser.add_argument('--history_url',
                        help='URL to the the history in JSON format',
                        default='https://marzzzello.gitlab.io/mirror-monitor/history.json')
    parser.add_argument('-d', '--directory',
                        help='output directory',
                        default='public')
    parser.add_argument('--wiki',
                        help='Include repos from https://forum.f-droid.org/t/known-repositories/721',
                        action='store_true')
    parser.add_argument('-t', '--threads',
                        help='Number of parallel threads when checking mirrors',
                        choices=range(1, 10), type=int,
                        default=5)
    parser.add_argument('--timeout',
                        help='Timeout for requests (seconds)',
                        type=int,
                        default=60)
    parser.add_argument('--trim',
                        help='Trim history entries to the last x hours',
                        type=int,
                        default=24*7)
    parser.add_argument('-v', '--verbosity',
                        help='Set verbosity level',
                        choices=['warning', 'info', 'debug'],
                        default='info')
    args = parser.parse_args()

    output_dir = path.realpath(args.directory)

    # init logger
    log = get_logger(__name__, args.verbosity)
    log.debug('logging is set to debug')

    if args.html:
        with open(output_dir + '/status.json', 'r') as fp:
            status = json.load(fp)
            website.create_html(status=status, dir=output_dir)
            exit(0)

    # if args.mirrors:
    #     mirrors = args.mirrors.split(',')
    # else:
    #     log.info('Collecting mirrors')
    #     mirrors = collect.mirrors()

    # if args.repos:
    #     log.info('Collecting repos')
    #     mirrors += collect.repos()

    # log.debug('mirrors: %s', mirrors)

    # official  mirrors
    repo_mirrors, archive_mirrors = get_mirrors_readme()

    # official repo
    official_fp = '43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB'
    url = 'https://f-droid.org/repo'
    official_repo = repo.Repo(url, fingerprint=official_fp)
    official_repo.set_additional_mirrors(repo_mirrors)
    # success = official_repo.get_all()
    # if success is False:
    #     exit('Error: https://f-droid.org/repo')

    # url_archive = 'https://f-droid.org/archive'
    # official_repo_archive = repo.Repo(url_archive, fingerprint=official_fp)
    # official_repo_archive.set_additional_mirrors(archive_mirrors)
    # success = official_repo_archive.get_all()
    # if success is False:
    #     exit('Error: https://f-droid.org/archive')

    #################################
    # run all mirror tests as threads
    mirrors = mirror.Mirror.instances
    timestamp = int(datetime.now(timezone.utc).timestamp())

    def worker(q, exceptions):
        while not q.empty():
            time.sleep(1)
            mirror_obj = q.get()
            threading.currentThread().name = mirror_obj.name
            try:
                mirror_obj.run_all()
                q.task_done()
            except Exception as e:
                log.fatal(e)
                log.error(traceback.format_exc())
                exceptions[mirror_obj.name] = e
                q.task_done()

    # put all mirrors in queue
    jobs = Queue()
    for mirror_obj in mirrors:
        jobs.put(mirror_obj)

    exceptions = {}
    # start threads
    for i in range(args.threads):
        t = threading.Thread(target=worker, args=(jobs, exceptions,), daemon=True)
        t.start()

    # wait for threads to finish
    jobs.join()

    for t in exceptions:
        log.fatal('Exception in thread %s: %s' % (t, exceptions[t]))
    if len(exceptions) > 0:
        exit(1)

    ###############
    # create status
    mirror_reports = []
    for mirror_obj in mirrors:
        mirror_reports.append(mirror_obj.get_data())

    status = dict()
    status['version'] = metadata(__package__)['Version']
    status['last_check'] = timestamp
    status['check_ip'] = get_own_ip()
    status['check_country'], status['check_country_code'] = geoip(status['check_ip'])
    status['mirrors'] = mirror_reports

    makedirs(output_dir, exist_ok=True)

    ##################################################
    # create history, add historical context to status
    h = None
    if args.no_history is False:
        log.info('Adding report to history')
        try:
            h = history.History(args.history_url)
            log.debug('The history had %s entries', len(h.history))
        except Exception as e:
            log.warning(str(e))
            log.error('Could not fetch history from %s', args.history_url)
            log.info('Creating empty history')
            h = history.History()

        h.add(status, timestamp)
        h.trim(args.trim)

        if len(h.history) == 1:
            log.debug('After trimming to the last %s hours the history has %s entry', args.trim, len(h.history))
        else:
            log.debug('After trimming to the last %s hours the history has %s entries', args.trim, len(h.history))

        h.save(path.join(args.directory, 'history.json'))
        status = h.historical_status(args.trim)
    ##################################################

    # save status.json
    with open(path.join(output_dir, 'status.json'), 'w') as fp:
        json.dump(status, fp)

    # create HTMLs
    if args.no_html is False:
        log.info('Creating HTMLs')
        website.create_html(status=status, dir=output_dir, history=h)

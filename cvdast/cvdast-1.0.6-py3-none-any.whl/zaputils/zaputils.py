# !/usr/bin/env python
import time
import datetime
import requests
import subprocess
import os
from pprint import pprint
from time import sleep
from zapv2 import ZAPv2 as ZAP

zap_proxy = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
zap = ZAP(proxies=zap_proxy)

def zap_open_url():
    cmd = "/Applications/OWASP_ZAP.app/Contents/Java/zap.sh -config api.disablekey=true -port {0}".format(
        8080
    )
    subprocess.Popen(cmd.split(" "), stdout=open(os.devnull, "w"))
    while True:
        try:
            status_req = requests.get("http://127.0.0.1:8080")
            if status_req.status_code == 200:
                break
        except Exception:
            pass
    print("ZAP opened!")
    sleep(3)

def zap_upload_script(name, file):
    data = {
        'scriptName': name,
        'scriptType': 'httpsender',
        'scriptEngine': 'Oracle Nashorn',
        'fileName': file,
        'scriptDescription': '',
        'charset': ''
    }

    response = requests.post('http://127.0.0.1:8080/JSON/script/action/load/', data=data)

    print(response.status_code)

def zap_enable_script(script_name):
    data = {
        'scriptName': script_name
    }

    response = requests.post('http://127.0.0.1:8080/JSON/script/action/enable/', data=data)
    print(response.status_code)

def zap_add_header(key, value):
    requests.get('http://127.0.0.1:8080/JSON/script/action/setGlobalVar/?varKey=cv-header&varValue={"'+str(key)+'":"'+str(value)+'"}')
    print("header added")

def zap_spider_target(target_url):
    print('Spidering target {}'.format(target_url))
    # The scan returns a scan id to support concurrent scanning
    scanID = zap.spider.scan(target_url)
    while int(zap.spider.status(scanID)) < 100:
        # Poll the status until it completes
        print('Spider progress %: {}'.format(zap.spider.status(scanID)))
        time.sleep(1)

    print('Spider has completed!')
    # Prints the URLs the spider has crawled
    print('\n'.join(map(str, zap.spider.results(scanID))))


def zap_active_scan(target_url):
    # TODO : explore the app (Spider, etc) before using the Active Scan API, Refer the explore section
    print('Active Scanning target {}'.format(target_url))
    scanID = zap.ascan.scan(target_url)
    while int(zap.ascan.status(scanID)) < 100:
        # Loop until the scanner has finished
        print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
        time.sleep(5)

    print('Active Scan completed')
    # Print vulnerabilities found by the scanning
    print('Hosts: {}'.format(', '.join(zap.core.hosts)))
    print('Alerts: ')
    pprint(zap.core.alerts(baseurl=target_url))


def ascan_status(scan_id):
    while int(zap.ascan.status(scan_id)) < 100:
        print(
            "Active Scan running at {}%".format(
                int(zap.ascan.status(scan_id))
            )
        )
        sleep(5)

def zap_enable_all_pscanners():
    requests.get("http://127.0.0.1:8080/JSON/pscan/action/enableAllScanners/?")

def export_zap_report(target):
    zap = ZAP(apikey=None)
    # Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
    # zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

    # TODO: Check if the scanning has completed

    # Retrieve the alerts using paging in case there are lots of them
    st = 0
    pg = 5000
    alert_dict = {}
    alert_count = 0
    alerts = zap.alert.alerts(baseurl=target, start=st, count=pg)
    blacklist = [1, 2]
    print(alerts)
    while len(alerts) > 0:
        #print('Reading ' + str(pg) + ' alerts from ' + str(st))
        alert_count += len(alerts)
        for alert in alerts:
            print(alert)
            plugin_id = alert.get('pluginId')
            if plugin_id in blacklist:
                continue
            if alert.get('risk') == 'High':
                # Trigger any relevant postprocessing
                continue
            if alert.get('risk') == 'Informational':
                # Ignore all info alerts - some of them may have been downgraded by security annotations
                continue
        st += pg
        alerts = zap.alert.alerts(start=st, count=pg)
    print('Total number of alerts: ' + str(alert_count))

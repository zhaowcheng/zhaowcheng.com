#!/bin/env python

import sys
import re
import gzip
import csv

import requests


def get_iploc_from_taobao(ip):
    resp = requests.get('http://ip.taobao.com/outGetIpInfo?ip=%s&accessKey=alibaba-inc' % ip)
    if resp.status_code != 200:
        raise requests.HTTPError(resp.status_code)
    else:
        if resp.json()['code'] != 0:
            raise Exception(resp.json()['msg'])
    data = resp.json()['data']
    return '%s - %s - %s' % (data['country'], data['region'], data['city'])


def get_iploc_from_ipapi(ip):
    resp = requests.get('http://ip-api.com/json/%s?lang=zh-CN' % ip)
    if resp.status_code != 200:
        raise requests.HTTPError(resp.status_code)
    else:
        if resp.json()['status'] != 'success':
            raise Exception(resp.json()['message'])
    data = resp.json()
    return '%s - %s - %s' % (data['country'], data['regionName'], data['city'])


def get_iploc_from_useragentinfo(ip):
    resp = requests.get('https://ip.useragentinfo.com/json?ip=' + ip)
    if resp.status_code != 200:
        raise requests.HTTPError(resp.status_code)
    else:
        if resp.json()['desc'] != 'success':
            raise Exception(resp.json()['message'])
    data = resp.json()
    return '%s - %s - %s' % (data['country'], data['province'], data['city'])


if len(sys.argv) != 3:
    print('Usage: %s <nginx_log> <output_csv>' % sys.argv[0])
    sys.exit(1)

nginx_log = sys.argv[1]
output_csv = sys.argv[2]
headers = ['ip', 'location', 'time', 'path', 'referer', 'log']
rows = []
openfunc = gzip.open if nginx_log.endswith('.gz') else open
with openfunc(nginx_log) as fp:
    for line in fp.readlines():
        m = re.search(r'GET (/posts/\S+/|/stylesheets/resumecards.css|/resume.pdf)', line)
        if m:
            segs = line.split()
            ip = segs[0]
            time = segs[3].replace('[', '')
            path = segs[6]
            referer = segs[10].replace('"', '')
            print('Processing: %s "%s"' % (ip, m.group(0)))
            location = get_iploc_from_useragentinfo(ip)
            rows.append({
                'ip': ip, 
                'location': location, 
                'time': time,
                'path': path,
                'referer': referer,
                'log': line
            })

with open(output_csv, 'a+') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writerows(rows)

print('write to %s success.' % output_csv)

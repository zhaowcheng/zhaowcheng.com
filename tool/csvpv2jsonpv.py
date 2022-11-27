#!/bin/env python

import sys
import csv
import json


if len(sys.argv) != 3:
    print('Usage: %s <csv_file> <output_file>' % sys.argv[0])
    sys.exit(1)

csv_file = sys.argv[1]
output_file = sys.argv[2]
pageviews = {}
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['path'] not in pageviews:
            pageviews[row['path']] = 1
        else:
            pageviews[row['path']] += 1

pageviews_for_chirpy = {'rows': []}
for k, v in pageviews.items():
    pageviews_for_chirpy['rows'].append([k, str(v)])

with open(output_file, 'w') as f:
    json.dump(pageviews_for_chirpy, f, indent=2)

print('write to %s success.' % output_file)

# -*- coding: utf-8 -*-

import sys
import csv

res = csv.writer(open(sys.argv[2], 'wt'))

data = list(csv.reader(open(sys.argv[1], 'rt')))
offset = -1
for i in xrange(len(data)):
    row = data[i]
    try:
        nrow = data[i+1]
    except:
        nrow = [''] * 10
    if offset == -1:
        offset = 0
        while row[offset] == '': offset += 1
    if row[offset+0] == 'День':
        continue
    elif ''.join(row) == '':
        continue
    elif nrow[offset+0] == 'День':
        group_name = row[offset+0]
        day = 'Пн'
        continue
    if row[offset+0] != '':
        day = row[offset+0]
        pair_number = 'все'
        weeks = 'все'
    else:
        row[offset+0] = day
    if row[offset+1] != '':
        pair_number = row[offset+1]
    else:
        row[offset+1] = pair_number
    if row[offset+2] != '':
        weeks = row[offset+2]
    else:
        row[offset+2] = weeks

    res.writerow([group_name] + row[offset:])
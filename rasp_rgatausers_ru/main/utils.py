# -*- coding: utf-8 -*-
from _curses import pair_number

from main.models import *

import csv


def parse_pairs_fa(str):
    """
     0 - Все
     1 - Нечетные
     2 - Четные
     3 - Все (с диапазоном)
     4 - список
    """
    str = str.replace(' ', '').replace('н', 'n').replace('ч', 'c').replace('в', 'v').replace('.', ',') + '#'
    s = 0
    buf = ''
    lst = []
    for c in str:
        if s == 0:
            if c == 'v':
                return 0, []
            elif c.isdigit():
                s = 1
                buf += c
        elif s == 1:
            if c.isdigit():
                buf += c
            elif c == ',':
                lst.append(int(buf))
                buf = ''
                s = 3
            elif c == '-':
                lst.append(int(buf))
                buf = ''
                s = 2
            elif c == "#":
                return 4, [int(buf)]
        elif s == 2:
            if c.isdigit():
                buf += c
            elif c == 'n':
                lst.append(int(buf))
                return 1, lst
            elif c == 'c':
                lst.append(int(buf))
                return 2, lst
            elif c == 'v':
                lst.append(int(buf))
                return 3, lst
        elif s == 3:
            if c.isdigit():
                buf += c
            elif c == ',':
                lst.append(int(buf))
                buf = ''
            elif c == '#':
                lst.append(int(buf))
                return 4, lst


def expand_list(t, _b=1, _e=17):
    code, r = t
    if code == 0:
        return range(_b, _e + 1)
    elif code == 1 or code == 2:
        return range(r[0], r[1] + 1, 2)
    elif code == 3:
        return range(r[0], r[1] + 1)
    elif code == 4:
        return r


def parse_pairs(s, _b=1, _e=17):
    try:
        return [expand_list(parse_pairs_fa(x), _b, _e) for x in s.split('/')]
    except:
        return [['']]


def import_csv(fn):
    for row in csv.reader(open(fn, 'rt')):
        try:
            group = Group.objects.get_or_create(name=row[0])[0]
            day = Day.objects.get_or_create(name=row[1])[0]
            dol = row[9]
            caf = Caf.objects.get_or_create(name=row[10])[0]
            if row[8] == '':
                prep = None
            else:
                try:
                    prep = Prep.objects.get(name=row[8])
                except:
                    prep = Prep(name=row[8], caf=caf, dol=dol)
                    prep.save()
            StandPair(
                group=group,
                day=day,
                prep=prep,
                subgroup=row[4],
                pair_number=row[2],
                week=row[3],
                pair_type=row[5],
                subject=row[6],
                aud=row[7],
            ).save()
            pair_numbers = [PairNumber.objects.get_or_create(num=x)[0] for x in parse_pairs(row[2], 0, 0)[0]]
            row[3].replace('Для', 'для')
            if row[3].find("для") != -1:
                row[3], row[4] = row[3].split('для')
                subgroups = [[SubGroup.objects.get_or_create(name=row[4], group=group)[0]]]
            else:
                subgroups = [[SubGroup.objects.get_or_create(name=x, group=group)[0] for x in y] for y in parse_pairs(row[4])]
            weeks = [[Week.objects.get_or_create(num=x)[0] for x in y] for y in parse_pairs(row[3])]
            pair_type = PairType.objects.get_or_create(name=row[5])[0]
            subject = Subject.objects.get_or_create(name=row[6])[0]
            aud = Aud.objects.get_or_create(name=row[7])[0]
            lst = map(None, weeks, subgroups)
            for item in lst:
                pair = Pair(
                    group=group,
                    day=day,
                    subgroup=item[1][0],
                    pair_type=pair_type,
                    subject=subject,
                    aud=aud,
                    prep=prep,
                )
                pair.save()
                weeks = item[0]
                for week in weeks:
                    pair.week.add(week)
                for pair_number in pair_numbers:
                    pair.pair_number.add(pair_number)
        except:
            for r in row:
                print r,
            print
#            raise

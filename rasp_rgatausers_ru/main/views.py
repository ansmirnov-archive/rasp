# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
import models
import datetime


def groups_list(request):
    return render_to_response('groups_list.html', {
        'groups': models.Group.objects.all().order_by('name'),
    })


def preps_list(request):
    return render_to_response('preps_list.html', {
        'preps': models.Prep.objects.all().order_by('name'),
    })


start_semester = datetime.date(2014, 2, 10)


def dcmp(x, y):
    ax = x.pair_numbers()
    ay = y.pair_numbers()
    if ax > ay:
        return 1
    elif ax < ay:
        return -1
    else:
        return 0


def gen_pair_list(req, id, week_id=1):
    #TODO: генерация week
    def c_filter(pair_set, group=None, prep=None):
        if group is not None:
            pair_set = pair_set.filter(group=group)
        if prep is not None:
            pair_set = pair_set.filter(prep=prep)
        return pair_set
    id = int(id)
    #group_id, prep_id = None, None
    if req == 'group':
        group = models.Group.objects.get(id=id)
        prep = None
        title = 'Расписание группы %s РГАТУ' % group.name.encode('utf-8')
    elif req == 'prep':
        group = None
        prep = models.Prep.objects.get(id=id)
        title = 'Расписание преподавателя %s РГАТУ' % prep.name.encode('utf-8')
    else:
        return
    week_id = int(week_id)
    db_days = models.Day.objects.all()
    c_date = start_semester + datetime.timedelta(days=(week_id-1)*7)
    days = []
    for day in db_days:
        pairs = []
        for pair in c_filter(day.pair_set, group, prep):
            if len(pair.week.filter(num=week_id)) > 0:
                pairs.append(pair)
        pairs.sort(cmp=dcmp)
        t = (day.name, pairs, c_date)
        if len(t[1]) > 0:
            days.append(t)
        c_date += datetime.timedelta(days=1)
    return {
        'title': title,
        'req': req,
        'id': id,
        'group': group,
        'days': days,
        'cur_week': models.Week.objects.get(id=week_id),
        'weeks': models.Week.objects.all(),
    }


def pairs_list(request, req, id, week_id=1):
    return render_to_response('%s.html' % req, gen_pair_list(req, id, week_id))


def pair_date(date, pair_number):
    start = datetime.datetime(date.year, date.month, date.day)
    min_pair = min([x.num for x in pair_number])
    max_pair = max([x.num for x in pair_number])
    if min_pair == 0 or max_pair == 0:
        start = start.replace(hour=0, minute=0)
        end = start + datetime.timedelta(1)
        return (start, end)
    if min_pair == 1:
        start = start.replace(hour=8, minute=30)
    elif min_pair == 2:
        start = start.replace(hour=10, minute=15)
    elif min_pair == 3:
        start = start.replace(hour=12, minute=40)
    elif min_pair == 4:
        start = start.replace(hour=14, minute=25)
    elif min_pair == 5:
        start = start.replace(hour=16, minute=10)
    elif min_pair == 6:
        start = start.replace(hour=18, minute=00)
    elif min_pair == 7:
        start = start.replace(hour=20, minute=30)
    end = start + datetime.timedelta(minutes=95*(max_pair-min_pair+1))
    return (start, end)


def ical(request, req, id):
    plist = gen_pair_list(req, id, 1)
    days = plist['days']
    for week in xrange(2, 3):
        days.extend(gen_pair_list(req, id, week)['days'])
    res = []
    for day in days:
        date = day[2]
        for pair in day[1]:
            adate = pair_date(date, pair.pair_number.all())
            res.append({
                'start': adate[0],
                'end': adate[1],
                'pair': pair,
            })
    return render_to_response('ical.html', {
        'list': res,
    })


def table(request):
    preps = []
    for prep in models.Prep.objects.all()[:3]:
        pairs = []
        for pair_number in models.PairNumber.objects.all().order_by('num'):
            dpairs = prep.pair_set.filter(pair_number=pair_number)
            pairs.append((pair_number.num, [dpairs.filter(week__id=week.id) for week in models.Week.objects.all()[:3]]))
        preps.append((prep.name, pairs))
    return render_to_response('table.html', {'preps': preps})


def stand(request):
    groups = []
    for group in models.Group.objects.all().order_by('name')[:10]:
        pairs = []
        for day in models.Day.objects.all():
            d = list(group.standpair_set.filter(day=day).order_by('pair_number'))
            pairs.append((day, d, len(d)))
        groups.append((group.name, pairs))
    return render_to_response('stand.html', {'groups': groups})

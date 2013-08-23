# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
import utils
import models
import datetime


def import_csv_view(request):
    utils.import_csv()
    return render_to_response('blank.html', {})


def groups_list(request):
    return render_to_response('groups_list.html', {
        'groups': models.Group.objects.all().order_by('name'),
    })


def preps_list(request):
    return render_to_response('preps_list.html', {
        'preps': models.Prep.objects.all().order_by('name'),
    })


start_semester = datetime.date(2013, 9, 2)


def dcmp(x, y):
    ax = x.pair_numbers()
    ay = y.pair_numbers()
    if ax > ay:
        return 1
    elif ax < ay:
        return -1
    else:
        return 0


def pairs_list(request, req, id, week_id=1):
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
    return render_to_response('%s.html' % req, {
        'title': title,
        'req': req,
        'id': id,
        'group': group,
        'days': days,
        'cur_week': models.Week.objects.get(id=week_id),
        'weeks': models.Week.objects.all(),
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
# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import *

@power_required([None])
def show(req):
    groups = []
    for gp in ProgramGroup.objects.order_by("order"):
        groups.append({'id':gp.id, 'title':gp.title})
    series = []
    for gs in ProgramSeries.objects.order_by("order"):
        series.append({'id':gs.id, 'title':gs.title})
    liwidth = 99 / len(groups)
    return render_to_response("resource/resource.html",
                              {'groups':groups, 'series': series, 'liwidth': liwidth},
                              context_instance=RequestContext(req));

@power_required([None])
def list_all(req):
    res = []
    for pg in Program.objects.order_by('-weight'):
        res.append(pg.id)
    return HttpResponse(json.dumps({'pid':res}), content_type='application/json')

@power_required([None])
def group_filter(req, arg):
    res = []
    for pg in ProgramGroup.objects.get(id=int(arg)).program.all().order_by('-weight'):
        res.append(pg.id)
    return HttpResponse(json.dumps({'pid':res}), content_type='application/json')

@power_required([None])
def get_arr(req):
    res = []
    pid = req.POST.getlist(u'pid[]', [])
    for i in range(0, len(pid)):
        pid[i] = int(pid[i])
    pgs = Program.objects.filter(id__in=pid)
    for pg in pgs:
        tmp = {}
        tmp['title'] = pg.title;
        tmp['description'] = None;
        tmp['group'] = None;
        tmp['series'] = None;
        tmp['recorder'] = None;
        tmp['contributor'] = None;
        tmp['workers'] = None;
        tmp['keyword'] = None;
        tmp['create_time'] = pg.create_time.strftime("%Y-%m-%d %H:%I:%S");
        if (pg.group):
            tmp['group'] = pg.group.title
        if (pg.series):
            tmp['series'] = pg.series.title
        if (pg.description):
            tmp['description'] = pg.description
        if (pg.recorder):
            tmp['recorder'] = pg.recorder
        if (pg.contributor):
            tmp['contributor'] = pg.contributor
        if (pg.workers):
            tmp['workers'] = pg.workers
        if (pg.keyword):
            tmp['keyword'] = pg.keyword
        res.append(tmp)
    return HttpResponse(json.dumps({'program':res}),
                        content_type='application/json')

@power_required([None])
def getarr_test(req):
    return render_to_response("resource/getarr_test.html",
                              context_instance=RequestContext(req));

@power_required([None])
def result(req):
    wd = req.POST.get('wd', None)
    res = []
    for pg in Program.objects.order_by('-weight'):
        res.append(pg.id)
    return render_to_response("resource/result.html",
                              {'pid':json.dumps(res)},
                              context_instance=RequestContext(req));
                              
@power_required([None])
def sort(req):
    pids = req.GET.getlist(u'pid[]', [])
    pids_i = []
    for id in pids:
        id = int(id)
        pids_i.append(id)
    sort = req.GET.get('sort')
    print pids
    pgs = Program.objects.filter(id__in=pids).order_by(sort);
    res = []
    for pg in pgs:
        res.append(pg.id);
    return HttpResponse(json.dumps({'pid':res}),
                        content_type='application/json')
                        
@power_required([None])
def filter(req):
    gids = req.GET.get('groupid')
    if gids == '-':
        gids = ProgramGroup.objects.order_by("order").values('id');
    sids = req.GET.get('seriesid')
    if sids == '-':
        sids = ProgramSeries.objects.order_by("order").values('id');
    pgids = [];
    pgs = Program.objects.filter(group__id in gids, series__id in sids).values('id');
    for pg in pgs:
        pgids.append(pg.id);
    srs = Program.objects.filter(group__id in gids).values('series').distinct();
    print pgids
    return HttpResponse(json.dumps({'pgs':pgids, 'srs':srs}),
                        content_type='application/json')
# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
from django.db.models import Q
import json

from models import *

@power_required([None])
def show(req):
    groups = []
    for gp in ProgramGroup.objects.filter(order__gte=0).order_by("-order"):
        groups.append({'id':gp.id, 'title':gp.title})
    series = []
    for gs in ProgramSeries.objects.filter(order__gte=0).order_by("-order"):
        series.append({'id':gs.id, 'title':gs.title})
    liwidth = 99 / len(groups)
    try:
        user = User.objects.get(id=req.session['uid'])
    except Exception, e:
        user = None
    return render_to_response("resource/resource.html",
                              {'groups':groups, 'series': series, 'liwidth': liwidth, 'logined':not (user == None)},
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
    pids = req.POST.getlist(u'pid[]', [])
    pgs = []
    try:
        user = User.objects.get(id=req.session['uid'])
    except Exception, e:
        user = None
    for pid in pids:
        pgs.append(Program.objects.get(id=int(pid)))
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
        tmp['have_praised'] = False;
        tmp['have_favorited'] = False;
        tmp['praise_count'] = pg.praise.count(),
        tmp['favorite_count'] = pg.favorite.count(),
        tmp['logined'] = not (user == None);
        tmp['create_time'] = pg.create_time.strftime("%Y-%m-%d %H:%I:%S");
        if not (user == None):
            tmp['have_praised'] = Praise.objects.filter(user=user, program=pg).count() > 0
            tmp['have_favorited'] = Favorite.objects.filter(user=user, program=pg).count() > 0
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
def sort(req):
    pids = req.GET.getlist(u'pid[]', [])
    pids_i = []
    for id in pids:
        id = int(id)
        pids_i.append(id)
    sort = req.GET.get('sort')
    res = []
    for pg in Program.objects.filter(id__in=pids).order_by(sort):
        res.append(pg.id);
    return HttpResponse(json.dumps({'pid':res}),
                        content_type='application/json')
                        
@power_required([None])
def filter(req):
    gid = req.GET.get('groupid')
    sid = req.GET.get('seriesid')
    keyword = req.GET.get('keyword')
    if keyword == None:
        keyword = '';
    if sid == '-' and gid == '-' and keyword == '':
        pgs = Program.objects.all();
    elif sid == '-' and keyword == '':
        pgs = Program.objects.filter(group__id=gid);
    elif gid == '-' and keyword == '':
        pgs = Program.objects.filter(series__id=sid);
    elif keyword == '':
        pgs = Program.objects.filter(group__id=gid, series__id=sid);
    elif sid == '-' and gid == '-':
        pgs = Program.objects.filter(Q(title__contains=keyword) |
                                     Q(description__contains=keyword) |
                                     Q(group__title__contains=keyword) |
                                     Q(series__title__contains=keyword));
    elif sid == '-':
        pgs = Program.objects.filter(Q(group__id=gid),
                                     Q(title__contains=keyword) |
                                     Q(description__contains=keyword) |
                                     Q(group__title__contains=keyword) |
                                     Q(series__title__contains=keyword));
    elif gid == '-':
        pgs = Program.objects.filter(Q(series__id=sid),
                                     Q(title__contains=keyword) |
                                     Q(description__contains=keyword) |
                                     Q(group__title__contains=keyword) |
                                     Q(series__title__contains=keyword));
    else:
        pgs = Program.objects.filter(Q(group__id=gid),
                                     Q(series__id=sid),
                                     Q(title__contains=keyword) |
                                     Q(description__contains=keyword) |
                                     Q(group__title__contains=keyword) |
                                     Q(series__title__contains=keyword));
    pgids = []
    for pg in pgs:
        pgids.append(pg.id);
    srres = []
    srs = []
    if gid == '-':
        tmp = ProgramSeries.objects.all()
        for i in tmp:
            srs.append({'series':i.id})
    else:
        srs = Program.objects.filter(group__id=gid).exclude(series=None).values('series').distinct();
    for sr in srs:
        srobj = ProgramSeries.objects.get(id=sr['series']);
        tmp = {};
        tmp['id'] = srobj.id;
        tmp['title'] = srobj.title;
        srres.append(tmp);
    return HttpResponse(json.dumps({'pid':pgids, 'srs':srres}),
                        content_type='application/json')

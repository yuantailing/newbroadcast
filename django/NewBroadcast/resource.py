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
    try:
        user = User.objects.get(id=req.session['uid'])
    except Exception, e:
        user = None
    return render_to_response("resource/resource.html",
                              {'groups':groups, 'series': series, 'logined': not(user == None)},
                              context_instance=RequestContext(req));

@power_required([None])
def list_all(req):
    res = []
    for pg in Program.objects.order_by('-weight', '-create_time'):
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
    pgss = Program.objects.filter(id__in=pids)
    for pid in pids:
        pgs.append(pgss.get(id=int(pid)))
    for pg in pgs:
        tmp = {}
        tmp['title'] = pg.title;
        tmp['id'] = pg.id;
        tmp['medialink'] = None;
        tmp['group'] = None;
        tmp['series'] = None;
        tmp['group_id'] = None;
        tmp['series_id'] = None;
        tmp['recorder'] = None;
        tmp['keyword'] = None;
        tmp['have_praised'] = False;
        tmp['have_favorited'] = False;
        tmp['praise_count'] = pg.praise.count();
        tmp['favorite_count'] = pg.favorite.count();
        tmp['logined'] = not (user == None);
        tmp['create_time'] = pg.create_time.strftime("%Y-%m-%d %H:%I:%S");
        if not (user == None):
            tmp['have_praised'] = Praise.objects.filter(user=user, program=pg).count() > 0
            tmp['have_favorited'] = Favorite.objects.filter(user=user, program=pg).count() > 0
        if (pg.audio):
            tmp['medialink'] = Source.objects.get(id=pg.audio).document.url
        if (pg.group):
            tmp['group'] = pg.group.title
        if (pg.series):
            tmp['series'] = pg.series.title
        if (pg.group):
            tmp['group_id'] = pg.group.id
        if (pg.series):
            tmp['series_id'] = pg.series.id
        if (pg.recorder):
            tmp['recorder'] = pg.recorder
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
    if sort == 'recorder_pinyin' or sort == '-recorder_pinyin':
        rs0 = Program.objects.filter(id__in=pids, recorder__isnull=True).order_by('-create_time').only('id')
        rs1 = Program.objects.filter(id__in=pids, recorder__isnull=False).order_by(sort).only('id')
        for pg in rs1:
            res.append(pg.id)
        for pg in rs0:
            res.append(pg.id)
    elif sort == 'series' or sort == '-series':
        rs0 = Program.objects.filter(id__in=pids, series__isnull=True).order_by('-create_time').only('id')
        rs1 = Program.objects.filter(id__in=pids, series__isnull=False).order_by(sort).only('id')
        for pg in rs1:
            res.append(pg.id)
        for pg in rs0:
            res.append(pg.id)
    else:
        rs = Program.objects.filter(id__in=pids).order_by(sort).only('id')
        for pg in rs:
            res.append(pg.id)
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
        pgs = Program.objects.filter(Q(keyword__contains=keyword));
    elif sid == '-':
        pgs = Program.objects.filter(Q(group__id=gid),
                                     Q(keyword__contains=keyword));
    elif gid == '-':
        pgs = Program.objects.filter(Q(series__id=sid),
                                     Q(keyword__contains=keyword));
    else:
        pgs = Program.objects.filter(Q(group__id=gid),
                                     Q(series__id=sid),
                                     Q(keyword__contains=keyword));
    pgids = []
    for pg in pgs.only('id'):
        pgids.append(pg.id);
    srres = []
    srs = []
    if gid == '-':
        tmp = ProgramSeries.objects.all()
        for i in tmp:
            srs.append(i.id)
    else:
        for i in Program.objects.filter(group__id=gid).exclude(series=None).values('series').distinct():
            srs.append(i['series'])
    for srobj in ProgramSeries.objects.filter(id__in=srs).order_by('-order'):
        tmp = {};
        tmp['id'] = srobj.id;
        tmp['title'] = srobj.title;
        srres.append(tmp);
    return HttpResponse(json.dumps({'pid':pgids, 'srs':srres}),
                        content_type='application/json')

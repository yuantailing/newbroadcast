# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import *
def show(req):
    groups = []
    for gp in ProgramGroup.objects.order_by("order"):
        groups.append({'id':gp.id, 'title':gp.title})
    liwidth = 99 / len(groups)
    return render_to_response("resource/resource.html",
                              {'groups':groups, 'liwidth': liwidth},
                              context_instance=RequestContext(req));

def list_all(req):
    res = []
    for pg in Program.objects.order_by('-weight'):
        res.append(pg.id)
    return HttpResponse(json.dumps({'pid':res}), content_type='application/json')

def group_filter(req, arg):
    res = []
    for pg in ProgramGroup.objects.get(id=int(arg)).program.all().order_by('-weight'):
        res.append(pg.id)
    return HttpResponse(json.dumps({'pid':res}), content_type='application/json')

def get_arr(req):
    res = []
    pid = req.POST.getlist(u'pid[]', [])
    for i in range(0, len(pid)):
        pid[i] = int(pid[i])
    pgs = Program.objects.filter(id__in=pid)
    print pgs
    for pg in pgs:
        group_title = None
        if (pg.group):
            group_title = pg.group.title
        res.append({'title':pg.title, 'group':group_title, 'series':pg.series})
    return HttpResponse(json.dumps({'program':res}),
                        content_type='application/json')

def getarr_test(req):
    return render_to_response("resource/getarr_test.html",
                              context_instance=RequestContext(req));

def result(req):
    wd = req.POST.get('wd', None)
    res = []
    for pg in Program.objects.order_by('-weight'):
        res.append(pg.id)
    return render_to_response("resource/result.html",
                              {'pid':json.dumps(res)},
                              context_instance=RequestContext(req));


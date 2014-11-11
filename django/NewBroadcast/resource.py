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
    return render_to_response("resource/resource.html", context_instance=RequestContext(req));

def list_all(req):
    res = []
    for pg in Program.objects.all():
        res.append(pg.id)
    return HttpResponse(json.dumps({'pid':res}), content_type='application/json')

def get_arr(req):
    res = []
    pid = req.POST.getlist(u'pid[]', [])
    for i in pid:
        pg = Program.objects.get(id=int(i))
        sn = {'title':pg.title, 'group':pg.group.title, 'series':pg.series}
        res.append(sn)
    return HttpResponse(json.dumps({'program':res}),
                        content_type='application/json')

def getarr_test(req):
    return render_to_response("resource/getarr_test.html",
                              context_instance=RequestContext(req));

# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import *

def show_program(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id=pgid)

    title = ""
    if pg.title:
        title = pg.title

    description = ""
    if pg.description:
        description = pg.description

    table = []
    if pg.group:
        table.append((u"节目组别", pg.group.title))
    if pg.series:
        table.append((u"节目系列", pg.series))
    if pg.recorder:
        table.append((u"录音/播音人员名单", pg.recorder))
    if pg.contributor:
        table.append((u"稿件来源", pg.contributor))
    if pg.workers:
        table.append((u"机务人员", pg.workers))

    piclink = []
    if pg.picture:
        pic_arr = json.loads(pg.picture)
        for i in pic_arr:
            piclink.append(Source.objects.get(id=i).document.url)
    
    medialink = ""
    if pg.audio:
        medialink = Source.objects.get(id=pg.audio).document.url
    
    return render_to_response("program/show.html",
                    {'pgid':pgid, 'title':title,
                     'strong':description[0:1], 'description':description[1:],
                     'medialink':medialink, 'piclink':piclink,
                     'table':table},
                    context_instance=RequestContext(req));

def play_program(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id=pgid)
    medialink = ""
    if pg.audio:
        medialink = Source.objects.get(id=pg.audio).document.url
    return render_to_response("program/player.html",
                              {'medialink':medialink},
                              context_instance=RequestContext(req));

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
    return render_to_response("program/getarr_test.html",
                              context_instance=RequestContext(req));

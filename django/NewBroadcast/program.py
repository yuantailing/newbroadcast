# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
from django import forms
import json
import os
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

    doc_links = []
    if pg.document:
        doc_arr = json.loads(pg.document)
        for i in range(0, len(doc_arr)):
            src = Source.objects.get(id=doc_arr[i])
            if i == 0:
                doc_links.append((u"资料下载", src.document.url, u"资料" + str(i + 1) + u": " +
                                  os.path.split(src.document.file.name)[1]))
            else:
                doc_links.append((u"", src.document.url, u"资料" + str(i + 1) + u": " +
                                  os.path.split(src.document.file.name)[1]))

    return render_to_response("program/show.html",
                    {'pgid':pgid, 'title':title,
                     'strong':description[0:1], 'description':description[1:],
                     'medialink':medialink, 'piclink':piclink,
                     'table':table, 'doc_links':doc_links},
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


def show_upload(req):
    result = req.GET.get('result', None)
    if result == 'success':
        result = u'上传成功'
    elif result == 'failed':
        result = u'操作失败'
    return render_to_response("program/upload.html",
                              {'result':result},
                              context_instance=RequestContext(req))


def upload_program(req):
    res = { }
    try:
        prg = Program()

        tgroup = req.POST.get('group', None)
        tseries = req.POST.get('series', None)
        ttitle = req.POST.get('title', None)
        tdescription = req.POST.get('description', None)
        tweight = req.POST.get('weight', None)
        trecorder = req.POST.get('recorder', None)
        tpicture = req.FILES.get('picture', None) # json of list
        taudio = req.FILES.get('audio', None)
        tdocument = req.POST.get('document', None) # json of list
        if (tgroup != None):
            prg.group = tgroup
        if (tseries != None):
            prg.series = tseries
        if (ttitle != None):
            prg.title = ttitle
        if (tdescription != None):
            prg.description = tdescription
        if (tweight != None):
            prg.weight = tweight
        if (trecorder != None):
            prg.recorder = trecorder
        if (tpicture != None):
            pic = Source()
            pic.document = tpicture
            pic.save()
            prg.picture = json.dumps([pic.id])
        if (taudio != None):
            ad = Source()
            ad.document = taudio
            ad.save()
            prg.audio = ad.id
        if (tdocument != None):
            prg.document = tdocument
        prg.save()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponseRedirect('/program/upload/?result=' + res['result'])


def show_modify(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id=pgid)

    title = ""
    if pg.title:
        title = pg.title

    description = ""
    if pg.description:
        description = pg.description

    piclink = []
    if pg.picture:
        pic_arr = json.loads(pg.picture)
        for i in pic_arr:
            piclink.append(Source.objects.get(id=i).document.url)
    
    medialink = ""
    if pg.audio:
        medialink = Source.objects.get(id=pg.audio).document.url

    return render_to_response("program/modify.html",
                    {'pgid':pgid, 'title':title,
                     'description':description,
                     'medialink':medialink, 'piclink':piclink}, 
                     context_instance=RequestContext(req));


def modify_word(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id = pgid)

    try:
        res = { }
        ttitle = req.POST.get('title', None)
        tdescription = req.POST.get('description', None)
        if (ttitle != None):
            pg.title = ttitle
        if (tdescription != None):
            pg.description = tdescription
        pg.save()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')


def modify_audio(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id = pgid)

    try:
        res = { }
        taudio = req.FILES.get('audio', None)
        ad = Source()
        ad.document = taudio
        ad.save()
        pg.audio = ad.id
        pg.save()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')


def modify_pic(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id = pgid)

    try:
        res = { }
        tpic = req.FILES.get('picture', None)
        pic = Source()
        pic.document = tpic
        pic.save()
        pg.picture = json.dumps([pic.id])
        pg.save()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')


def delete_program(req, arg):
    res = { }
    try:
        prgid = int(arg)
        prg = Program.objects.get(id = prgid)
        prg.delete()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')

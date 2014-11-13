# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import

def modifyProgram(req):
    res = { }
    try:
        prgid = req.POST.get('id', None)
        prg = Program.objects.get(id = prgid)

        tgroup = req.POST.get('group', None)
        tseries = req.POST.get('series', None)
        ttitle = req.POST.get('title', None)
        tdescription = req.POST.get('description', None)
        tweight = req.POST.get('weight', None)
        trecorder = req.POST.get('recorder', None)
        tpicture = req.POST.get('picture', None) # json of list
        taudio = req.POST.get('audio', None)
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
            prg.picture = tpicture
        if (taudio != None):
            prg.audio = taudio
        if (tdocument != None):
            prg.document = tdocument
        prg.save()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')


def uploadProgram(req):
    res = { }
    try:
        prg = Program()

        tgroup = req.POST.get('group', None)
        tseries = req.POST.get('series', None)
        ttitle = req.POST.get('title', None)
        tdescription = req.POST.get('description', None)
        tweight = req.POST.get('weight', None)
        trecorder = req.POST.get('recorder', None)
        tpicture = req.POST.get('picture', None) # json of list
        taudio = req.POST.get('audio', None)
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
            prg.picture = tpicture
        if (taudio != None):
            prg.audio = taudio
        if (tdocument != None):
            prg.document = tdocument
        prg.save()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')


def deleteProgram(req):
    res = { }
    try:
        prgid = req.POST.get('id', None)
        prg = Program.objects.get(id = prgid)
        prg.delete()
        res['result'] = 'success'
    except Exception, e:
        res['result'] = 'failed'
    return HttpResponse(json.dumps(res), content_type='application/json')

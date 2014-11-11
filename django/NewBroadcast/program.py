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
    if description:
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

    piclink = "/static/images/1.jpg"
    
    medialink = u"/upload/source/sample.mp3"
    
    return render_to_response("program/show.html",
                    {'pgid':pgid, 'title':title,
                     'strong':description[0:1], 'description':description[1:],
                     'medialink':medialink, 'piclink':piclink,
                     'table':table},
                    context_instance=RequestContext(req));

def play_program(req, arg):
    return render_to_response("program/player.html", context_instance=RequestContext(req));

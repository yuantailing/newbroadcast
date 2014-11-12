# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
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

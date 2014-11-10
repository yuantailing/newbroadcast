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
    # pg = Program.objects.get(id=pgid)
    title = u"海燕 - 高尔基"
    description = u"此文按海面景象的发展变化分成三部分，描绘了海燕面临狂风暴雨和波涛翻腾的大海时的壮丽图画。在这篇文章中，作者通过对海燕在暴风雨来临之际勇敢欢乐的形象的描写，深刻反映了1905年俄国革命前夕急剧发展的革命形势，热情歌颂了俄国无产阶级革命先驱坚强无畏的战斗精神"
    medialink = u"/upload/source/sample.mp3"
    table = [(u"播音人员", u"这里填录音/播音人员名单"),
             (u"稿件来源", u"这里填稿件来源"),
             (u"机务人员", u"这里填机务人员名单")]
    piclink = "/static/images/1.jpg"
    return render_to_response("program/show.html",
                    {'pgid':pgid, 'title':title,
                     'strong':description[0:1], 'description':description[1:],
                     'medialink':medialink, 'piclink':piclink,
                     'table':table},
                    context_instance=RequestContext(req));

def play_program(req, arg):
    return render_to_response("program/player.html", context_instance=RequestContext(req));

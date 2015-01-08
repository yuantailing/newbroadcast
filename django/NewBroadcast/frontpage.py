# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from .models import *


def show_index(req):
    return render_to_response(
        "frontpage/index.html",
        context_instance=RequestContext(req))


@power_required([None])
def waterflow_data(req):
    s_w = req.GET.get('s_w')
    e_w = req.GET.get('e_w')
    obj = Program.objects.order_by("-weight", "-create_time")[s_w: e_w]
    ret = []
    for o in obj:
        tmpret = {}
        tmpret['id'] = o.id
        pic_arr = json.loads(o.picture)
        try:
            s = Source.objects.get(id=pic_arr[0])
            if s.thumb:
                s.thumb.file
                tmpret['src'] = s.thumb.url
            else:
                s.document.file
                tmpret['src'] = s.document.url
        except Exception as e:
            tmpret['src'] = "/static/images/default.jpg"
        tmpret['title'] = o.title
        tmpret['content'] = o.description
        tmpret['canplay'] = not o.audio == None
        ret.append(tmpret)
    return HttpResponse(json.dumps(ret), content_type="application/json")

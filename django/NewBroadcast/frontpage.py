# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import *
def show_index(req):
    return render_to_response("frontpage/index.html", context_instance=RequestContext(req))

def waterflow_data(req):
    s_w = req.GET.get('s_w');
    e_w = req.GET.get('e_w');
    obj = Program.objects.order_by("-weight", "-click")[s_w: e_w];
    ret = [];
    for o in obj:
        tmpret = {};
        tmpret['id'] = o.id;
        pic_arr = json.loads(o.picture)
        if pic_arr and (len(pic_arr) > 0):
            tmpret['src'] = Source.objects.get(id=pic_arr[0]).document.url
        else:
            pass
        tmpret['title'] = o.title;
        tmpret['content'] = o.description;
        ret.append(tmpret);
    return HttpResponse(json.dumps(ret), content_type = "application/json");

def click(req):
    p_id = req.POST.get('id');
    p_click = req.POST.get('click');
    if p_click == '1':
        obj = Program.objects.get(id = p_id);
        obj.click += 1;
        obj.save();
    return HttpResponse(json.dumps([{"success":1}]), content_type = "application/json");

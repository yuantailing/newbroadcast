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
    
def add_program_group(req):
    res = { }
    try:
        p_title = req.POST.get('title', None)
        p_order = req.POST.get('order', None)
        try:
            pg = ProgramGroup.objects.get(title = p_title)
            if (user.password == p_password):
                res['success'] = True
                res['info'] = u'登录成功'
                req.session['uid'] = user.id
                req.session['user_nickname'] = user.nickname
                req.session['user_power'] = user.power
            else:
                res['success'] = False
                res['info'] = u'密码错误'
        except Exception, e:
            res['success'] = False
            res['info'] = u'用户不存在'
    except Exception, e:
        res['success'] = False
        res['info'] = u'未知错误'
    return HttpResponse(json.dumps(res), content_type='application/json')
    
def delete_program_group(req):
    p_id = req.POST.get('id');
    p_click = req.POST.get('click');
    p_weight = req.POST.get('weight');
    obj = Program.objects.get(id = p_id);
    obj.weight = p_weight;
    return HttpResponse(json.dumps([{"success":1}]), content_type = "application/json");
    
def change_program_group(req):
    p_id = req.POST.get('id');
    p_click = req.POST.get('click');
    p_weight = req.POST.get('weight');
    obj = Program.objects.get(id = p_id);
    obj.weight = p_weight;
    return HttpResponse(json.dumps([{"success":1}]), content_type = "application/json");
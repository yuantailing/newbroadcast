# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
from models import *
import json

def judge(req):
    res = { }
    try:
        t_key = req.POST.get('key', None)
        t_type = req.POST.get('ptype', None)
        if (t_type == 'nickname'):
            user = User.objects.get(nickname = t_key)
        else:
            user = User.objects.get(email = t_key)
        res['exist'] = 'true'
    except Exception, e:
        res['exist'] = 'false'
    return HttpResponse(json.dumps(res), content_type='application/json')

def do(req):
    res = { }
    try:
        user = User()
        p_email = req.POST.get('email', None)
        p_nickname = req.POST.get('nickname', None)
        p_password = req.POST.get('password', None)
        p_password2 = req.POST.get('password2', None)
        if (p_password == p_password2):
            user.email = p_email
            user.nickname = p_nickname
            user.password = p_password
            user.save()
            res['result'] = 'success'
            res['info'] = '注册成功'
            req.session['uid'] = user.id
        else:
            res['result'] = 'failed'
            res['info'] = '两次输入的密码不一致'
    except Exception, e:
        res['result'] = 'failed'
        res['info'] = '用户名或密码已存在'
    return HttpResponse(json.dumps(res), content_type='application/json')

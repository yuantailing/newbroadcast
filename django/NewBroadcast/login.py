# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json


from models import *


def do(req):
    res = { }
    try:
        p_email = req.POST.get('email', None)
        p_password = req.POST.get('password', None)
        try:
            user = User.objects.get(email=p_email)
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

def test(req):
    res = { }
    try:
        uid = req.session['uid']
        user = User.objects.get(id=uid)
        res['uid'] = user.id
        res['result'] = 'have_login'
    except Exception, e:
        res['result'] = 'not_login'
    return HttpResponse(json.dumps(res), content_type='application/json')

def logout(req):
    req.session.clear()
    return HttpResponseRedirect('/')


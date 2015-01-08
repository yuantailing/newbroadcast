# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json


from .models import *


@power_required([None])
def login(req):
    res = {}
    try:
        p_email = req.POST.get('email', None)
        p_password = req.POST.get('password', None)
        try:
            user = User.objects.get(email=p_email)
            if user.verify_password(p_password):
                res['success'] = True
                res['info'] = u'登录成功'
                req.session['uid'] = user.id
                req.session['user_power'] = user.power
            else:
                res['success'] = False
                res['info'] = u'密码错误'
        except Exception as e:
            res['success'] = False
            res['info'] = u'用户不存在'
    except Exception as e:
        res['success'] = False
        res['info'] = u'未知错误'
    return HttpResponse(json.dumps(res), content_type='application/json')


@power_required([None])
def test(req):
    res = {}
    try:
        uid = req.session['uid']
        user = User.objects.get(id=uid)
        res['login'] = True
        res['uid'] = user.id
    except Exception as e:
        res['login'] = False
    return HttpResponse(json.dumps(res), content_type='application/json')


@power_required([None])
def logout(req):
    req.session.clear()
    return HttpResponseRedirect('/')


@power_required([None])
def exist_judge(req):
    res = {}
    try:
        t_key = req.POST.get('key', None)
        t_type = req.POST.get('ptype', None)
        if (t_type == 'nickname'):
            user = User.objects.get(nickname=t_key)
        else:
            user = User.objects.get(email=t_key)
        res['exist'] = 'true'
    except Exception as e:
        res['exist'] = 'false'
    return HttpResponse(json.dumps(res), content_type='application/json')


@power_required([None])
def signin(req):
    res = {}
    try:
        user = User()
        p_email = req.POST.get('email', None)
        p_nickname = req.POST.get('nickname', None)
        p_password = req.POST.get('password', None)
        p_password2 = req.POST.get('password2', None)
        if '@' not in p_email:
            res['success'] = False
            res['info'] = u'邮箱格式错误'
        elif not p_nickname:
            res['success'] = False
            res['info'] = u'昵称不能为空'
        elif '@' in p_nickname:
            res['success'] = False
            res['info'] = u'昵称不能含@符号'
        elif not p_password:
            res['success'] = False
            res['info'] = u'密码不能为空'
        elif not p_password == p_password2:
            res['success'] = False
            res['info'] = u'两次输入的密码不一致'
        else:
            user.email = p_email
            user.nickname = p_nickname
            user.set_password(p_password)
            try:
                user.save()
                res['success'] = True
                res['info'] = u'注册成功'
                req.session['uid'] = user.id
                req.session['user_nickname'] = user.nickname
                req.session['user_power'] = user.power
            except Exception as e:
                res['success'] = False
                res['info'] = u'邮箱名/昵称错误'
    except Exception as e:
        res['success'] = False
        res['info'] = u'未知错误'
    return HttpResponse(json.dumps(res), content_type='application/json')

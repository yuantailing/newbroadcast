# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers

from models import *
import json

def power_trans(power_str):
    power_dic = {'user':u'普通用户',
                 'worker':u'台员',
                 'admin':u'管理员',
                 'superadmin':u'超级管理员',
                 }
    if power_str in power_dic:
        return power_dic[power_str]
    else:
        return u'未知权限'

@power_required(['user'])
def show_space(req):
    user = User.objects.get(id=req.session['uid'])
    ups = Program.objects.filter(uploader=user).order_by('-create_time')[0:5]
    return render_to_response("manager/space.html",
                              {'user':user,
                               'power':power_trans(user.power),
                               'ups':ups, },
                              context_instance=RequestContext(req));

@power_required(['worker'])
def show_mgrres(req):
    return render_to_response("manager/resource.html",
                              context_instance=RequestContext(req))

@power_required(['worker'])
def show_mgrmyres(req):
    return render_to_response("manager/myresource.html",
                              context_instance=RequestContext(req))

@power_required(['admin'])
def show_mgrallres(req):
    return render_to_response("manager/allresources.html",
                              context_instance=RequestContext(req))

@power_required(['superadmin'])
def show_mgruser(req):
    obj_list = User.objects.all()
    if req.REQUEST.get('wd', None):
        search = req.REQUEST.get('wd', None)
        g1 = obj_list.filter(email__contains=search)
        g2 = obj_list.filter(nickname__contains=search)
        g3 = obj_list.filter(power__contains=search)
        g4 = obj_list.filter(birthday__contains=search)
        g5 = obj_list.filter(phone_number__contains=search)
        obj_list = g1 | g2 | g3 | g4 | g5
    return render_to_response("manager/user.html",
                              {'obj_list':obj_list, },
                              context_instance=RequestContext(req))

@power_required(['user'])
def change_password(req):
    res = {}
    psw_old = req.POST.get('old_password', None)
    psw0 = req.POST.get('new_password', None)
    psw1 = req.POST.get('check_password', None)
    try:
        if psw0 and psw0 == psw1:
            user = User.objects.get(id=req.session['uid'])
            if user.password == psw_old:
                user.password = psw0
                user.save()
                res['success'] = True
                res['info'] = u'修改密码成功'
            else:
                res['success'] = False
                res['info'] = u'旧密码错误'
        else:
            res['success'] = False
            res['info'] = u'密码不一致'
    except Exception, e:
            res['success'] = False
            res['info'] = u'未知错误'
    return HttpResponse(json.dumps(res), content_type='application/json')

@power_required(['user'])
def change_info(req):
    res = {}
    nick = req.POST.get('nickname', None)
    birth = req.POST.get('birth', None)
    phone = req.POST.get('phone', None)
    try:
        try:
            user = User.objects.get(nickname=nick)
            print user
            if user.id == req.session['uid']:
                raise Exception
            res['success'] = False
            res['info'] = u'昵称已存在'
        except Exception, e:
            user = User.objects.get(id=req.session['uid'])
            if nick:
                user.nickname = nick
            user.birthday = birth
            if not birth:
                user.birthday = None
            user.phone_number = phone
            user.save()
            res['success'] = True
            res['info'] = u'修改资料成功'
    except Exception, e:
        res['success'] = False
        res['info'] = u'未知错误'
    return HttpResponse(json.dumps(res), content_type='application/json')


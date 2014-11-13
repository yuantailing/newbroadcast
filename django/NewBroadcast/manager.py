# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers

from models import *


def power_trans(power_str):
    print(power_str)
    power_dic = {'user':u'普通用户',
                 'worker':u'台员',
                 'admin':u'管理员',
                 'superadmin':u'超级管理员',
                 }
    if power_str in power_dic:
        return power_dic[power_str]
    else:
        return u'未知权限'

def show_space(req):
    user = User.objects.get(id=req.session['uid'])
    return render_to_response("manager/space.html",
                              {'user': user,
                               'power': power_trans(user.power)},
                              context_instance=RequestContext(req));

def show_mgrres(req):
    return render_to_response("manager/mgrres.html", context_instance=RequestContext(req));

def show_mgruser(req):
    return render_to_response("manager/mgruser.html", context_instance=RequestContext(req));

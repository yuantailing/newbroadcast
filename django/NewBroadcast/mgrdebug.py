# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json


from models import *


@power_required([None])
def change_power(req, arg):
    user = User.objects.get(id=int(req.session['uid']))
    req.session['user_power'] = arg
    user.power = arg
    user.save()
    return HttpResponse(arg)

@power_required([None])
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

@power_required(['user'])
def logout(req):
    req.session.clear()
    return HttpResponseRedirect('/')


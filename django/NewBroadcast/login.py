# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt

from models import *


def form(req):
    t = get_template("login/login_form.html")
    c = RequestContext(req);
    html = t.render(c)
    return HttpResponse(html)

@csrf_exempt
def do(req):
    res = { }
    try:
        p_email = req.POST.get('email', None)
        p_password = req.POST.get('password', None)
        user = User.objects.get(email=p_email)
        res = { }
        if (user.password == p_password):
            res['result'] = 'success'
            req.session['uid'] = user.id
        else:
            res['result'] = 'failed'
    except Exception, e:
        res['result'] = 'exception'
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
    res = { }
    req.session['uid'] = None
    res['result'] = 'success'
    return HttpResponse(json.dumps(res), content_type='application/json')


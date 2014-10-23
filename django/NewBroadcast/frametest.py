# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django import template
import datetime

def hello(req, str):
    return HttpResponse("<h1>Hello %s</h1>" % str);

def ctime(req):
    cutime = datetime.datetime.now()
    txt = "It's %s." % cutime
    return HttpResponse(txt)

def temp(req):
    str = "这是从.py文件传的字符串，作为模板参数"
    fp = open("templates/temp.html")
    t = template.Template(fp.read())
    fp.close()
    html = t.render(template.Context({'data': str}))
    return HttpResponse(html)

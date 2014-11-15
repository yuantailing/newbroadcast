# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import *
from hashlib import md5
from models import *

def getresult(req):
    txt = req.POST.get("input", None)
    return HttpResponse('<p>服务器端计算出输入的MD5值为（UTF-8编码） %s </p>' %
                        md5(txt.encode("utf-8")).hexdigest())

def index(req):
    # t = get_template("ajaxtest/index.html")
    # c = RequestContext(req)
    # return HttpResponse(t.render(c))
    return render_to_response("ajaxtest/index.html", context_instance=RequestContext(req))

def htmltest(req):
    return render_to_response("ajaxtest/htmltest.html", context_instance=RequestContext(req))

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

def htmlresponse(req):
    user = User.objects.get(id=req.session['uid'])
    print user.id
    return render_to_response("ajaxtest/htmlresponse.html",
                              {'user':user,
                               'power':power_trans(user.power)},
                              context_instance=RequestContext(req))

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def list_program(req):
    paginator = Paginator(Program.objects.all(), 4) # Show 25 contacts per page
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(req.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        pgs = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pgs = paginator.page(paginator.num_pages)

    return render_to_response("ajaxtest/listprogram.html",
                              {'all':Program.objects.all(),
                               'pgs':pgs, },
                              context_instance=RequestContext(req))


# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import *
from hashlib import md5

def getresult(req):
    txt = req.POST.get("input", None)
    return HttpResponse('<p>服务器端计算出输入的MD5值为（UTF-8编码） %s </p>' %
                        md5(txt.encode("utf-8")).hexdigest())

def index(req):
    # t = get_template("ajaxtest/index.html")
    # c = RequestContext(req)
    # return HttpResponse(t.render(c))
    return render_to_response("ajaxtest/index.html", context_instance=RequestContext(req))

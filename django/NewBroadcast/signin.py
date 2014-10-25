from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers

from models import *

class Signin:
    @classmethod
    def form(self, req):
        t = get_template("signin.html")
        c = RequestContext(req);
        html = t.render(c)
        return HttpResponse(html)
        # return render_to_response("signin.html", RequestContext(req))

    @classmethod
    def do(self, req):
        user = User();
        user.email = req.POST['email']
        user.password = req.POST['password']
        user.nickname = req.POST['nickname']
        user.phone_number = req.POST['phone_number']
        if not user.email:
            user.email = None
        if not user.password:
            user.password = None
        if not user.nickname:
            user.nickname = None
        if not user.phone_number:
            user.phone_number = None
        user.save();
        return HttpResponse(serializers.serialize('json',
                            User.objects.filter(id=user.id)))

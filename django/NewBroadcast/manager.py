# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers

from models import *
def show_space(req):
    return render_to_response("manager/space.html", context_instance=RequestContext(req));

def show_mgrres(req):
    return render_to_response("manager/mgrres.html", context_instance=RequestContext(req));

def show_mgruser(req):
    return render_to_response("manager/mgruser.html", context_instance=RequestContext(req));

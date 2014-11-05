# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import *
def show_index(req):
        t = get_template("frontpage/index.html")
        c = RequestContext(req);
        html = t.render(c)
        return HttpResponse(html)


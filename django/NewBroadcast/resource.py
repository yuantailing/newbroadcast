# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
import json

from models import *
def show(req, arg):
    return render_to_response("resource/resource.html", context_instance=RequestContext(req));

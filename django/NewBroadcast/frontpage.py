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
    return render_to_response("frontpage/index.html", {});
	
def waterflow_data(req):
	s_w = req.GET.get('s_w');
	e_w = req.GET.get('e_w');
	obj = Program.objects.order_by("weight")[s_w: e_w];
	ret = [];
	for o in obj:
		tmpret = {};
		pic = Source.objects.filter(program_id = o.picture_id, source_type = "picture")[0];
		tmpret["picture"] = pic.link;
	return HttpResponse(serializers.serialize('json', obj), content_type = "application/json");
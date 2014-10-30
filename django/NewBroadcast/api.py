import json
from django.db import models
from django.core import serializers
from django.http import HttpResponse

from models import *

def api_user(req):
	r_id = req.GET.get('id');
	obj = User.objects.get(id = r_id);
	return HttpResponse(serializers.serialize('json', [obj])[1 : -1], content_type = "application/json");

def api_program_group(req):
	r_id = req.GET.get('id');
	obj = ProgramGroup.objects.get(id = r_id);
	return HttpResponse(serializers.serialize('json', [obj])[1 : -1], content_type = "application/json");
	
def api_program_series(req):
	r_id = req.GET.get('id');
	obj = ProgramSeries.objects.get(id = r_id);
	return HttpResponse(serializers.serialize('json', [obj])[1 : -1], content_type = "application/json");
	
def api_program(req):
	r_id = req.GET.get('id');
	obj = Program.objects.get(id = r_id);
	return HttpResponse(serializers.serialize('json', [obj])[1 : -1], content_type = "application/json");

def api_source(req):
	r_id = req.GET.get('id');
	obj = Source.objects.get(id = r_id);
	return HttpResponse(serializers.serialize('json', [obj])[1 : -1], content_type = "application/json");

def api_comment(req):
	r_id = req.GET.get('id');
	obj = Comment.objects.get(id = r_id);
	return HttpResponse(serializers.serialize('json', [obj])[1 : -1], content_type = "application/json");
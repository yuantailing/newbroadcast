# -*- coding: UTF-8 -*-
from django.db import models
from django.core import serializers
from django.http import HttpResponse
from NewBroadcast.models import *
import json

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


import os

class ProgramLocalImporter:
    class SizeFile(file):
        def __init__(self, filename):
            file_size = os.path.getsize(filename);
            super(ProgramLocalImporter.SizeFile, self).__init__(filename, 'rb');
        def size(self):
            return self.file_size
    def set_title(self, title):
        self.title = title
    def set_picture_filename(self, name):
        self.picture_filename = name
    def save(self):
        pro = Program()
        pro.title = self.title
        if 'picture_filename' in dir(self):
            picture_file = ProgramLocalImporter.SizeFile(self.picture_filename)
            pro.picture.save(os.path.split(self.picture_filename)[1],
                             picture_file, save=False)
        pro.save()

'''
本地导入文件的方法：
运行manage.py shell
from NewBroadcast.api import ProgramLocalImporter
pp = ProgramLocalImporter()
pp.set_title('importer title here')
pp.set_picture_filename('static/images/1.jpg')
pp.save()

批量导入示例：
for i in range(1,11):
    pp = ProgramLocalImporter()
    pp.set_title('importer title here')
    pp.set_picture_filename('static/images/' + str(i) + '.jpg')
    pp.save()
'''

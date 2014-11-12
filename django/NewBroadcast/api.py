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
    def __init__(self):
        self.title = None
        self.group_id = None
        self.picture_arr = []
        self.audio_id = None
        self.document_arr = []
    def set_title(self, title):
        self.title = title
    def set_group(self, group_id):
        self.group_id = group_id
    def add_picture(self, name):
        src = Source()
        src.document.save(os.path.split(name)[1],
                          ProgramLocalImporter.SizeFile(name), save=False)
        src.save()
        self.picture_arr.append(src.id)
    def set_audio_filename(self, name):
        src = Source()
        src.document.save(os.path.split(name)[1],
                          ProgramLocalImporter.SizeFile(name), save=False)
        src.save()
        self.audio = src.id
    def add_document(self, name):
        src = Source()
        src.document.save(os.path.split(name)[1],
                          ProgramLocalImporter.SizeFile(name), save=False)
        src.save()
        self.document_arr.append(src.id)
    def save(self):
        pro = Program()
        pro.title = self.title
        pro.group = ProgramGroup.objects.get(id=self.group_id)
        pro.picture = json.dumps(self.picture_arr)
        pro.audio = self.audio_id
        pro.document = json.dumps(self.document_arr)
        pro.save()


'''
本地导入文件的方法：
运行manage.py shell
from NewBroadcast.api import ProgramLocalImporter
pp = ProgramLocalImporter()
pp.set_title('importer title here')
pp.set_group(2) # 假设存在group 2
pp.add_picture('static/images/' + str(2) + '.jpg')
pp.save()

批量导入示例：
from NewBroadcast.api import ProgramLocalImporter
for i in range(1,11):
    pp = ProgramLocalImporter()
    pp.set_title('importer title here')
    pp.set_group(2) # 假设存在group 2
    pp.add_picture('static/images/' + str(i) + '.jpg')
    pp.save()
'''

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

def find_session(key, value):
    for s in Session.objects.all():
        d = s.get_decoded()
        if key in d and d[key] == value:
            return s
    return None


def set_session(session, key, value):
    d = session.get_decoded()
    d[key] = value
    session.session_data = SessionStore().encode(d)
    session.save()

'''
异步设置用户session的方法示例：
sess = find_session('uid', 1)
set_session(sess, 'user_power', 'admin')
'''

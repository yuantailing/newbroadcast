# -*- coding: UTF-8 -*-
from django.db import models
from django.core import serializers
from django.http import HttpResponse
from NewBroadcast.models import *
import json
import os


class ProgramLocalImporter:

    class SizeFile(file):

        def __init__(self, filename):
            file_size = os.path.getsize(filename)
            super(ProgramLocalImporter.SizeFile, self).__init__(filename, 'rb')

        def size(self):
            return self.file_size

    def __init__(self):
        self.pro = Program()
        self.picture_arr = []
        self.document_arr = []

    def set_title(self, title):
        self.pro.title = title

    def set_description(self, description):
        self.pro.description = description

    def set_group(self, group_id):
        self.pro.group = ProgramGroup.objects.get(id=group_id)

    def set_series(self, group_id):
        self.pro.series = ProgramSeries.objects.get(id=group_id)

    def set_recorder(self, recorder):
        self.pro.recorder = recorder

    def set_contributor(self, contributor):
        self.pro.contributor = contributor

    def set_worker(self, worker):
        self.pro.worker = worker

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
        self.pro.audio = src.id

    def add_document(self, name):
        src = Source()
        src.document.save(os.path.split(name)[1],
                          ProgramLocalImporter.SizeFile(name), save=False)
        src.save()
        self.document_arr.append(src.id)

    def save(self):
        self.pro.picture = json.dumps(self.picture_arr)
        self.pro.document = json.dumps(self.document_arr)
        self.pro.save()


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
    pp.set_title('import title here')
    pp.set_description('在这叫喊声里——充满着对暴风雨的渴望！在这叫喊声里，乌云听出了愤怒的力量、热情的火焰和胜利的信心。海鸥在暴风雨来临之前呻吟着')
    pp.set_group(1) # 假设存在group 1
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

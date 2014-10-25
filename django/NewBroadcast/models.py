from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(blank = False, default = None, unique = True)
    password = models.TextField(blank = False, default = None)
    nickname = models.TextField(blank = False, default = None, unique = True)
    power = models.CharField(blank = False, default = 'user', max_length = 32, 
            choices = (('user','user'),('admin','admin'),
                       ('administrator','administrator')))
    birthday = models.DateTimeField(null = True, blank = True, default = None)
    phone_number = models.CharField(null = True, blank = True, default = None, max_length = 32)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class ProgramGroup(models.Model):
    title = models.TextField(blank = False, default = None)
    description = models.TextField(null = True, blank = True, default = None)
    weight = models.IntegerField(blank = False, default = 0)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class ProgramSeries(models.Model):
    group_id = models.IntegerField(blank = False, default = None, db_index = True)
    title = models.TextField(blank = False, default = None)
    description = models.TextField(null = True, blank = True, default = None)
    weight = models.IntegerField(blank = False, default = 0)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class Program(models.Model):
    series_id = models.IntegerField(blank = False, default = None, db_index = True)
    title = models.TextField(blank = False, default = None)
    description = models.TextField(null = True, blank = True, default = None)
    weight = models.IntegerField(blank = False, default = 0)
    page_format = models.TextField(null = True, blank = True, default = None)
    recorder = models.TextField(null = True, blank = True, default = None)
    source = models.TextField(null = True, blank = True, default = None)
    workers = models.TextField(null = True, blank = True, default = None)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class Source(models.Model):
    program_id = models.IntegerField(blank = False, default = None, db_index = True)
    source_type = models.TextField(blank = False, default = None)
    title = models.TextField(null = True, blank = True, default = None)
    description = models.TextField(null = True, blank = True, default = None)
    link = models.TextField(null = True, blank = True, default = None)
    doc = models.FileField(null = True, blank = True, default = None, upload_to = 'source/')
    weight = models.IntegerField(blank = False, default = 0)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    uid = models.IntegerField(blank = False, default = None, db_index = True)
    program_id = models.IntegerField(blank = False, default = None, db_index = True)
    content = models.TextField(blank = False, default = None)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

from django.contrib import admin
admin.site.register((User, ProgramGroup, ProgramSeries, Program,
                     Source, Comment))


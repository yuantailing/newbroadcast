from django.db import models


# Create your models here.

class User(models.Model):
    # uid = models.IntegerField(null = False, default = None, unique = True)
    mail = models.TextField(null = False, default = None, unique = True)
    password = models.TextField(null = False, default = None)
    nickname = models.TextField(null = False, default = None, unique = True)
    power = models.TextField(null = False, default = 'user')
    birthday = models.DateTimeField(null = True, default = None)
    phone_number = models.TextField(null = True, default = None)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class ProgramGroup(models.Model):
    title = models.TextField(null = False, default = None)
    description = models.TextField(null = True, default = None)
    weight = models.IntegerField(null = False, default = 0)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class ProgramSeries(models.Model):
    group_id = models.IntegerField(null = False, default = None)
    title = models.TextField(null = False, default = None)
    description = models.TextField(null = True, default = None)
    weight = models.IntegerField(null = False, default = 0)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class Program(models.Model):
    series_id = models.IntegerField(null = False, default = None)
    title = models.TextField(null = False, default = None)
    description = models.TextField(null = True, default = None)
    weight = models.IntegerField(null = False, default = 0)
    page_format = models.TextField(null = True, default = None)
    recorder = models.TextField(null = True, default = None)
    source = models.TextField(null = True, default = None)
    workers = models.TextField(null = True, default = None)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class Source(models.Model):
    program_id = models.IntegerField(null = False, default = None)
    source_type = models.TextField(null = False, default = None)
    title = models.TextField(null = True, default = None)
    description = models.TextField(null = True, default = None)
    link = models.TextField(null = True, default = None)
    weight = models.IntegerField(null = False, default = 0)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    uid = models.IntegerField(null = False, default = None)
    program_id = models.IntegerField(null = False, default = None)
    content = models.TextField(null = False, default = None)
    update_time = models.DateTimeField(auto_now_add = True, auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)


from django.contrib import admin


admin.site.register((User, ProgramGroup, ProgramSeries, Program,
                     Source, Comment))



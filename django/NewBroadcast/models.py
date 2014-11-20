from django.db import models
import thread
import os

# Create your models here.

class User(models.Model):
    email = models.EmailField(blank=False, default=None, unique=True)
    password = models.TextField(blank=False, default=None)
    nickname = models.CharField(blank=False, default=None, unique=True, max_length=128)
    power = models.CharField(blank=False, default='user', max_length=32,
                             choices=(('user', 'user'), ('worker', 'worker'),
                                      ('admin', 'admin'),
                                      ('superadmin', 'superadmin'),))
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    phone_number = models.CharField(null=True, blank=True, default=None,
                                    max_length=32)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + self.nickname + ' | ' + self.email

    def save(self):
        if not self.email:
            self.email = None
        if not self.password:
            self.password = None
        if not self.nickname:
            self.nickname = None
        if not self.power:
            self.power = None
        if not self.phone_number:
            self.phone_number = None
        super(User, self).save()


class ProgramGroup(models.Model):
    title = models.TextField(blank=False, default=None)
    order = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + self.title
    
    def save(self):
        if not self.title:
            self.title = None
        super(ProgramGroup, self).save()


class ProgramSeries(models.Model):
    title = models.TextField(blank=False, default=None)
    order = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + self.title
    
    def save(self):
        if not self.title:
            self.title = None
        super(ProgramSeries, self).save()


class Program(models.Model):
    group = models.ForeignKey(ProgramGroup, related_name="program",
                              null=True, blank=True, default=None,
                              on_delete=models.SET_NULL)
    series = models.ForeignKey(ProgramSeries, related_name="program",
                              null=True, blank=True, default=None,
                              on_delete=models.SET_NULL)
    title = models.TextField(blank=False, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    weight = models.IntegerField(blank=False, default=0)
    recorder = models.TextField(null=True, blank=True, default=None)
    contributor = models.TextField(null=True, blank=True, default=None)
    workers = models.TextField(null=True, blank=True, default=None)
    keyword = models.TextField(null=True, blank=True, default=None)
    picture = models.TextField(null=True, blank=True, default='[]') # json of list
    audio = models.IntegerField(null=True, blank=True, default=None)
    document = models.TextField(null=True, blank=True, default='[]') # json of list
    uploader = models.ForeignKey(User, related_name="program",
                              null=True, blank=True, default=None,
                              on_delete=models.SET_NULL)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        res = '[' + str(self.id) + '] ' + self.title
        if self.group:
            res += ' | ' + self.group.title
        if self.series:
            res += ' | ' + self.series.title
        return res
    
    def save(self):
        if not self.title:
            self.title = None
        if not self.description:
            self.description = None
        if not self.recorder:
            self.recorder = None
        if not self.contributor:
            self.page_format = None
        if not self.workers:
            self.workers = None
        if not self.picture:
            self.picture = None
        if not self.document:
            self.document = None
        self.keyword = self.title
        if self.description:
            self.keyword += '|' + self.description
        if self.recorder:
            self.keyword += '|' + self.recorder
        if self.contributor:
            self.keyword += '|' + self.contributor
        if self.workers:
            self.keyword += '|' + self.workers
        super(Program, self).save()


class Source(models.Model):
    document = models.FileField(null=True, blank=True, default=None,
                           upload_to='source')
    md5 = models.TextField(null=True, blank=True, default=None)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + os.path.split(self.document.path)[1]
    
    def save(self):
        if not self.md5:
            self.md5 = None
        super(Source, self).save()


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comment",
                              null=False, blank=False, default=None,
                              on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name="comment",
                              null=False, blank=False, default=None,
                              on_delete=models.CASCADE)
    content = models.TextField(blank=False, default=None)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + self.program.title + ' | ' + self.user.nickname
    
    def save(self):
        if not self.content:
            self.content = None
        super(Comment, self).save()


praise_lock = thread.allocate_lock()
class Praise(models.Model):
    user = models.ForeignKey(User, related_name="praise",
                              null=False, blank=False, default=None,
                              on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name="praise",
                              null=False, blank=False, default=None,
                              on_delete=models.CASCADE)
    # in Program filter: annotate(num_praise=Count('praise'))
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + self.program.title + ' | ' + self.user.nickname
    
    def save(self):
        try:
            praise_lock.acquire()
            ft = Praise.objects.filter(user=self.user, program=self.program)
            if ft.count() > 0:
                raise Exception
            super(Praise, self).save()
            praise_lock.release()
        except Exception, e:
            praise_lock.release()
            raise e


favorite_lock = thread.allocate_lock()
class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="favorite",
                              null=False, blank=False, default=None,
                              on_delete=models.CASCADE)
    program = models.ForeignKey(Program, related_name="favorite",
                              null=False, blank=False, default=None,
                              on_delete=models.CASCADE)
    # in Program filter: annotate(num_favorite=Count('favorite'))
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '[' + str(self.id) + '] ' + self.program.title + ' | ' + self.user.nickname

    def save(self):
        try:
            favorite_lock.acquire()
            ft = Favorite.objects.filter(user=self.user, program=self.program)
            if ft.count() > 0:
                raise Exception
            super(Favorite, self).save()
            favorite_lock.release()
        except Exception, e:
            favorite_lock.release()
            raise e

from django.http import HttpResponse
from django.shortcuts import *
def power_required(power_list):
    if None in power_list:
        power_list.append('')
    if '' in power_list:
        power_list.append('guest')
    if 'guest' in power_list:
        power_list.append('user')
    if 'user' in power_list:
        power_list.append('worker')
    if 'worker' in power_list:
        power_list.append('admin')
    if 'admin' in power_list:
        power_list.append('superadmin')
    def decorator(req_fun):
        def required_req(*args, **kwargs):
            req = args[0]
            power = req.session.get('user_power', None)
            try:
                user = User.objects.get(id=req.session.get('uid', None))
                if not user.power == power:
                    req.session['user_power'] = user.power
                    power = user.power
            except Exception, e:
                user = None
            if not power:
                req.session['user_power'] = 'guest'
                power = 'guest'
            accessed = False
            for allowed in power_list:
                if power == allowed:
                    accessed = True
                    break
                if not allowed and not power:
                    accessed = True
                    break
            if accessed:
                return req_fun(*args, **kwargs)
            else:
                return render_to_response("error/forbid-power-required.html",
                                          {'power_required':repr(power_list),
                                           'power_got':repr(power), },
                                          context_instance=RequestContext(req))
        return required_req
    return decorator

from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(blank=False, default=None, unique=True)
    password = models.TextField(blank=False, default=None)
    nickname = models.TextField(blank=False, default=None, unique=True)
    power = models.CharField(blank=False, default='user', max_length=32,
                             choices=(('user', 'user'), ('admin', 'admin'),
                                      ('administrator', 'administrator')))
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    phone_number = models.CharField(null=True, blank=True, default=None,
                                    max_length=32)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

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
    description = models.TextField(null=True, blank=True, default=None)
    weight = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.title:
            self.title = None
        if not self.description:
            self.description = None
        super(ProgramGroup, self).save()


class ProgramSeries(models.Model):
    group_id = models.IntegerField(blank=False, default=None, db_index=True)
    title = models.TextField(blank=False, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    weight = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.title:
            self.title = None
        if not self.description:
            self.description = None
        super(ProgramSeries, self).save()


class Program(models.Model):
    series_id = models.IntegerField(blank=False, default=None, db_index=True)
    title = models.TextField(blank=False, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    weight = models.IntegerField(blank=False, default=0)
    page_format = models.TextField(null=True, blank=True, default=None)
    recorder = models.TextField(null=True, blank=True, default=None)
    source_id = models.TextField(null=True, blank=True, default=None)
    workers = models.TextField(null=True, blank=True, default=None)
    picture_id = models.TextField(null=True, blank=True, default=None)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.title:
            self.title = None
        if not self.description:
            self.description = None
        if not self.page_format:
            self.page_format = None
        if not self.recorder:
            self.recorder = None
        if not self.source:
            self.source = None
        if not self.workers:
            self.workers = None
        super(Program, self).save()


class Source(models.Model):
    program_id = models.IntegerField(blank=False, default=None, db_index=True)
    source_type = models.TextField(blank=False, default=None)
    title = models.TextField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    link = models.TextField(null=True, blank=True, default=None)
    doc = models.FileField(null=True, blank=True, default=None,
                           upload_to='source/')
    weight = models.IntegerField(blank=False, default=0)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.title:
            self.title = None
        if not self.description:
            self.description = None
        if not self.source_type:
            self.source_type = None
        if not self.link:
            self.link = None
        super(Source, self).save()
		if self.source_type == "picture":
			o.["picture_id"] = self.id;
			o.save();
		if self.source_type == "program":
			o.["source_id"] = self.id;
			o.save();


class Comment(models.Model):
    uid = models.IntegerField(blank=False, default=None, db_index=True)
    program_id = models.IntegerField(blank=False, default=None, db_index=True)
    content = models.TextField(blank=False, default=None)
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        if not self.content:
            self.content = None
        super(Comment, self).save()

from django.contrib import admin
admin.site.register((User, ProgramGroup, ProgramSeries, Program,
                     Source, Comment))

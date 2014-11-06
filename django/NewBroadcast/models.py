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
    group = models.ForeignKey(ProgramGroup, related_name="series", blank=False)
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
    series = models.ForeignKey(ProgramSeries, related_name="program", blank=False)
    title = models.TextField(blank=False, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    weight = models.IntegerField(blank=False, default=0)
    page_format = models.TextField(null=True, blank=True, default=None)
    recorder = models.TextField(null=True, blank=True, default=None)
    workers = models.TextField(null=True, blank=True, default=None)
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
        if not self.workers:
            self.workers = None
        super(Program, self).save()

        
class Source(models.Model):
    program = models.ForeignKey(Program, related_name="source", unique=True);
    doc = models.FileField(null=True, blank=True, default=None,
                           upload_to='source/')
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
            

class Picture(models.Model):
    program = models.ForeignKey(Program, related_name="picture", unique=True);
    doc = models.FileField(null=True, blank=True, default=None,
                           upload_to='source/')
    update_time = models.DateTimeField(auto_now_add=True, auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)


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

# -*- coding: UTF-8 -*-
import unittest
import random
from models import *


class MakeDataTest(unittest.TestCase):
    def test_makedata(self):
        User(email='admin', nickname='admin', password='admin',
             power='superadmin').save()


class ModelsTest(unittest.TestCase):
    def test_user_normal_use(self):
        s = str(random.random())
        user = User()
        user.email = s
        user.nickname = s
        user.password = '123456'
        user.save()
    def test_user_just_empty(self):
        s = str(random.random())
        user = User()
        self.assertRaises(Exception, user.save)
    def test_user_sth_empty(self):
        s = str(random.random())
        user = User()
        user.email = s
        user.nickname = s
        user.password = ''
        self.assertRaises(Exception, user.save)
    def test_user_ununique_email(self):
        s = str(random.random())
        t = str(random.random())
        user = User()
        user.email = s
        user.nickname = s
        user.password = '123456'
        user.save()
        user = User()
        user.email = s
        user.nickname = t
        user.password = '123456'
        self.assertRaises(Exception, user.save)
    def test_user_ununique_nickname(self):
        s = str(random.random())
        t = str(random.random())
        user = User()
        user.email = s
        user.nickname = s
        user.password = '123456'
        user.save()
        user = User()
        user.email = t
        user.nickname = s
        user.password = '123456'
        self.assertRaises(Exception, user.save)
    def test_programgroup_normal_use(self):
        pg = ProgramGroup()
        pg.title = 'A'
        pg.description = 'B'
        pg.save()
    def test_programgroup_title_empty(self):
        pg = ProgramGroup()
        pg.title = ''
        pg.description = 'B'
        self.assertRaises(Exception, pg.save)
    def test_programgroup_desrip_empty(self):
        pg = ProgramGroup()
        pg.title = 'A'
        pg.save()


import login
import manage
from django.test.client import Client


class ManageTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ManageTest, self).__init__(*args, **kwargs)
    def test_login(self):
        global cl
        cl = Client()
        cl.post('/login/do/', {'email':'admin', 'password':'admin', })
        print cl.session.items()
    def test_show_space(self):
        global cl
        res = cl.get('/space/')
        self.assertTrue('<a href="/manage/user/">' in res.content)


import program

class ProgramTest(unittest.TestCase):
    pass


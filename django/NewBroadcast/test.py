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
import random
from django.test.client import Client


class PoweredClient(Client):
    def __init__(self, power):
        super(PoweredClient, self).__init__()
        users = User.objects.filter(power=power)
        if users.count() > 0:
            user = users.first()
            self.post('/login/do/', {'email': user.email, 'password': user.password,
                                     'power': power, })
        else:
            s = str(random.random())
            user = User(email=s + '@163.com', nickname=s, password='PoweredUser', )
            user.save()
            self.post('/login/do/', {'email':user.email, 'password':user.password, })
        assert self.session.get('user_power') == power


class ManageTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ManageTest, self).__init__(*args, **kwargs)
    def test_login(self):
        pc = PoweredClient('superadmin')
        print pc.session.items()
    def test_show_space(self):
        pc = PoweredClient('superadmin')
        res = pc.get('/space/')
        self.assertTrue('<a href="/manage/user/">' in res.content)


import program

class ProgramTest(unittest.TestCase):
    pass


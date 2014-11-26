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
import json
from django.test.client import Client


class PoweredClient(Client):
    def __init__(self, power):
        super(PoweredClient, self).__init__()
        users = User.objects.filter(power=power)
        if users.count() > 0:
            user = users.first()
            self.post('/login/do/', {'email': user.email, 'password': user.password, })
        else:
            s = str(random.random())
            user = User(email=s + '@163.com', nickname=s, password=s,
                        power=power, )
            user.save()
            self.post('/login/do/', {'email':user.email, 'password':user.password, })
        assert self.session.get('user_power') == power


class ManageTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ManageTest, self).__init__(*args, **kwargs)
    def test_login(self):
        pc = PoweredClient('superadmin')
    def test_power_trans(self):
        from manage import power_trans
        self.assertEqual(u'普通用户', power_trans(u'user'))
        self.assertEqual(u'台员', power_trans(u'worker'))
        self.assertEqual(u'管理员', power_trans(u'admin'))
        self.assertEqual(u'超级管理员', power_trans(u'superadmin'))
        self.assertEqual(u'未知权限', power_trans(u''))
    def test_show_space(self):
        pc = PoweredClient('superadmin')
        res = pc.get('/space/')
        self.assertTrue('<a href="/manage/user/">' in res.content)
        pc = PoweredClient('admin')
        res = pc.get('/space/')
        self.assertFalse('<a href="/manage/user/">' in res.content)
        pc = Client()
        res = pc.get('/space/')
        self.assertTrue('forbidden' in res.content)
    def test_show_favorites(self):
        pc = PoweredClient('user')
        res = pc.get('/manage/favorites/')
        self.assertTrue('/manage/favorites/table/' in res.content)
        res = pc.get('/manage/favorites/table/')
        self.assertTrue('我的收藏' in res.content)
    def test_show_mgrres(self):
        pc = PoweredClient('user')
        res = pc.get('/manage/resource/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('worker')
        res = pc.get('/manage/resource/')
        self.assertTrue('forbidden' not in res.content)
    def test_show_mgrmyres(self):
        pc = PoweredClient('user')
        res = pc.get('/manage/myresource/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('worker')
        res = pc.get('/manage/myresource/')
        self.assertTrue('forbidden' not in res.content)
    def test_show_mgrallres(self):
        pc = PoweredClient('worker')
        res = pc.get('/manage/allresources/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('admin')
        res = pc.get('/manage/allresources/')
        self.assertTrue('forbidden' not in res.content)
    def test_show_mgruser(self):
        pc = PoweredClient('admin')
        res = pc.get('/manage/user/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('superadmin')
        res = pc.post('/manage/user/', {'wd': 'admin'})
        self.assertTrue('forbidden' not in res.content)
    def test_change_password(self):
        pc = PoweredClient('user')
        uid = int(pc.session.get('uid'))
        user = User.objects.get(id=uid)
        res = pc.post('/manage/changepassword/',
                      {'old_password': 'abcdefg', 'new_password': 'newpassword',
                       'check_password': 'newpassword', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/changepassword/',
                      {'old_password': user.password, 'new_password': 'newpassword',
                       'check_password': 'checkpassword', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/changepassword/',
                      {'old_password': user.password, 'new_password': 'newpassword',
                       'check_password': 'newpassword', })
        self.assertEqual(True, json.loads(res.content)['success'])
        
        
    


import program

class ProgramTest(unittest.TestCase):
    pass


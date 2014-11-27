# -*- coding: UTF-8 -*-
import unittest
import random
from models import *

'''
# 测试模型（不充分的测试）
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
'''

import login
import manage
import json
from django.test.client import Client


# 先访问login以获取权限的Client类
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

'''
# 对manage.py的充分测试
class ManageTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ManageTest, self).__init__(*args, **kwargs)

    # 测试权限翻译内容
    def test_power_trans(self):
        from manage import power_trans
        self.assertEqual(u'普通用户', power_trans(u'user'))
        self.assertEqual(u'台员', power_trans(u'worker'))
        self.assertEqual(u'管理员', power_trans(u'admin'))
        self.assertEqual(u'超级管理员', power_trans(u'superadmin'))
        self.assertEqual(u'未知权限', power_trans(u''))

    # 测试个人空间显示逻辑
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

    # 测试收藏夹显示
    def test_show_favorites(self):
        pc = PoweredClient('user')
        res = pc.get('/manage/favorites/')
        self.assertTrue('/manage/favorites/table/' in res.content)
        res = pc.get('/manage/favorites/table/')
        self.assertTrue('我的收藏' in res.content)

    # 测试台员上传管理
    def test_show_mgrres(self):
        pc = PoweredClient('user')
        res = pc.get('/manage/resource/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('worker')
        res = pc.get('/manage/resource/')
        self.assertTrue('forbidden' not in res.content)

    # 测试台员"我的上传"
    def test_show_mgrmyres(self):
        pc = PoweredClient('user')
        res = pc.get('/manage/myresource/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('worker')
        res = pc.get('/manage/myresource/')
        self.assertTrue('forbidden' not in res.content)

    # 测试管理员"所有上传"
    def test_show_mgrallres(self):
        pc = PoweredClient('worker')
        res = pc.get('/manage/allresources/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('admin')
        res = pc.get('/manage/allresources/')
        self.assertTrue('forbidden' not in res.content)

    # 测试超级管理员用户列表
    def test_show_mgruser(self):
        pc = PoweredClient('admin')
        res = pc.get('/manage/user/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('superadmin')
        res = pc.post('/manage/user/', {'wd': 'admin'})
        self.assertTrue('forbidden' not in res.content)

    # 测试修改密码
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

    # 测试修改个人信息
    def test_change_info(self):
        pc = PoweredClient('user')
        uid = int(pc.session.get('uid'))
        user = User.objects.get(id=uid)
        # 昵称重复
        User(email='abcdefg@163.com', nickname='repeated_3322635',
             password='123456').save()
        res = pc.post('/manage/changeinfo/',
                      {'nickname': 'repeated_3322635', 'birth': '1995-01-01',
                       'phone': '18811432211', })
        self.assertEqual(False, json.loads(res.content)['success'])
        # 昵称含@
        res = pc.post('/manage/changeinfo/',
                      {'nickname': 'abc@cde', 'birth': '1995-01-01',
                       'phone': '18811432211', })
        self.assertEqual(False, json.loads(res.content)['success'])
        # 生日格式错误
        res = pc.post('/manage/changeinfo/',
                      {'nickname': str(random.random()), 'birth': '1',
                       'phone': '18811432211', })
        self.assertEqual(False, json.loads(res.content)['success'])
        # 昵称不变，正确
        res = pc.post('/manage/changeinfo/',
                      {'nickname': user.nickname, 'birth': '1995-01-01',
                       'phone': '18811432211', })
        self.assertEqual(True, json.loads(res.content)['success'])
        # 不修改生日和电话
        res = pc.post('/manage/changeinfo/',
                      {'nickname': str(random.random()), 'birth': '',
                       'phone': '', })
        self.assertEqual(True, json.loads(res.content)['success'])

    # 测试修改权限
    def test_change_power(self):
        pc = PoweredClient('superadmin')
        pc2 = PoweredClient('user')
        uid = int(pc.session.get('uid'))
        uid2 = int(pc2.session.get('uid'))
        user = User.objects.get(id=uid)
        user2 = User.objects.get(id=uid2)
        # 用户不存在
        res = pc.post('/manage/changepower/',
                      {'uid': 99999, 'new_power': 'worker', })
        self.assertEqual(False, json.loads(res.content)['success'])
        # 不允许修改自己的权限
        res = pc.post('/manage/changepower/',
                      {'uid': uid, 'new_power': 'worker', })
        self.assertEqual(False, json.loads(res.content)['success'])
        # 不合法的新权限
        res = pc.post('/manage/changepower/',
                      {'uid': 2, 'new_power': 'not_a_power', })
        self.assertEqual(False, json.loads(res.content)['success'])
        # 正确
        res = pc.post('/manage/changepower/',
                      {'uid': uid2, 'new_power': 'worker', })
        self.assertEqual(True, json.loads(res.content)['success'])
    def test_groupseries(self):
        pc = PoweredClient('admin')
        res = pc.get('/manage/groupseries/')
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('superadmin')
        res = pc.get('/manage/groupseries/')
        self.assertTrue('forbidden' not in res.content)
    def test_program_group(self):
        # 获取节目组别页面
        pc = PoweredClient('superadmin')
        res = pc.get('/manage/groupseries/group/')
        self.assertEqual(200, res.status_code)
        # 修改组别
        pg = ProgramGroup(title="new_program_group")
        pg.save()
        res = pc.post('/manage/groupseries/group/',
                      {'id': 99999, 'action': 'modify',
                       'new_name': 'new_group', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'id': 1, 'action': 'modify'})
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'id': pg.id, 'action': 'modify',
                       'new_name': 'new_group', })
        # 增加组别（增加组别id为2）
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'action': 'add',
                       'new_name': '', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'action': 'add',
                       'new_name': 'add_group_name', })
        self.assertEqual(True, json.loads(res.content)['success'])
        # 删除组别
        res = pc.post('/manage/groupseries/group/',
                      {'id': 99999, 'action': 'delete', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'id': 2, 'action': 'delete', })
        self.assertEqual(True, json.loads(res.content)['success'])
        # 恢复组别
        res = pc.post('/manage/groupseries/group/',
                      {'id': 99999, 'action': 'restore', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'id': 2, 'action': 'restore', })
        self.assertEqual(True, json.loads(res.content)['success'])
        # 彻底删除组别
        pro = Program(title="new_program", group_id=2)
        pro.save()
        res = pc.post('/manage/groupseries/group/',
                      {'id': 99999, 'action': 'destroy', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'id': 2, 'action': 'destroy', })
        self.assertEqual(False, json.loads(res.content)['success'])
        pro.delete()
        res = pc.post('/manage/groupseries/group/',
                      {'id': 2, 'action': 'destroy', })
        self.assertEqual(True, json.loads(res.content)['success'])
        # 组别排序
        res = pc.post('/manage/groupseries/group/',
                      {'new_order': 1, 'action': 'sort', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'new_order[]': [1, 2, ], 'action': 'sort', })
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/manage/groupseries/group/',
                      {'new_order[]': [1, ], 'action': 'sort', })
        self.assertEqual(True, json.loads(res.content)['success'])
        
    def test_program_series(self):
        pc = PoweredClient('superadmin')
        res = pc.get('/manage/groupseries/series/')
        self.assertEqual(200, res.status_code)
        # 测试增加系列
        res = pc.post('/manage/groupseries/series/',
                      {'action': 'add',
                       'new_name': 'add_group_name', })
        self.assertEqual(True, json.loads(res.content)['success'])
'''

import program

class ProgramTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ProgramTest, self).__init__(*args, **kwargs)

    def test_show_program(self):
        pro = Program(title='program1')
        pro.description = 'desc'
        pg = ProgramGroup(title='group1')
        pg.save()
        ps = ProgramSeries(title='series1')
        ps.save()
        pro.group = pg
        pro.series = ps
        pro.recorder = 'recorder'
        pro.contributor = 'contributor'
        pro.workers = 'workers'
        from api import ProgramLocalImporter
        source1 = Source()
        source1.document.save('test_not_pic.js',
                              ProgramLocalImporter.SizeFile('static/js/csrfajax.js'))
        source2 = Source()
        source2.document.save('test_pic.jpg',
                              ProgramLocalImporter.SizeFile('static/images/1.jpg'))
        pro.picture = json.dumps([source1.id, source2.id])
        pro.audio = source1.id
        pro.document = json.dumps([source1.id, source2.id])
        pro.save()
        pc = PoweredClient('user')
        res = pc.get('/program/' + str(pro.id))
        self.assertEqual(200, res.status_code)
    def test_play_program(self):
        pc = PoweredClient('user')
        res = pc.get('/program/play/1')
        self.assertEqual(200, res.status_code)
    def test_praise(self):
        pro = Program(title="praise_program")
        pro.save()
        pc = PoweredClient('user')
        res = pc.post('/program/praise/', {'pid': pro.id})
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/program/praise/', {'pid': pro.id})
        self.assertEqual(False, json.loads(res.content)['success'])
    def test_unparise(self):
        pro = Program(title="praise_program")
        pro.save()
        pc = PoweredClient('user')
        res = pc.post('/program/praise/', {'pid': pro.id})
        res = pc.post('/program/unpraise/', {'pid': pro.id})
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/program/unpraise/', {'pid': 'abc'})
        self.assertEqual(False, json.loads(res.content)['success'])
    def test_favorite(self):
        pc = PoweredClient('user')
        res = pc.post('/program/favorite/', {'pid': 1})
        self.assertEqual(200, res.status_code)
    def test_unfavorite(self):
        pc = PoweredClient('user')
        res = pc.post('/program/unfavorite/', {'pid': 1})
        self.assertEqual(200, res.status_code)
    def test_add_comment_del_comment(self):
        pro = Program(title="comment_program")
        pro.save()
        pc = PoweredClient('user')
        res = pc.post('/program/comment/add/', {'pid': pro.id, 'comment':'abc'})
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/program/comment/add/', {'pid': pro.id, 'comment':'abcdefg'})
        self.assertEqual(True, json.loads(res.content)['success'])
        pc = PoweredClient('superadmin')
        res = pc.post('/program/comment/del/', {'cid':99999})
        self.assertEqual(False, json.loads(res.content)['success'])
        pc = PoweredClient('superadmin')
        res = pc.post('/program/comment/del/', {'cid':Comment.objects.first().id})
        self.assertEqual(True, json.loads(res.content)['success'])
    def test_show_upload(self):
        pc = PoweredClient('worker')
        res = pc.get('/program/upload/?result=success')
        self.assertEqual(200, res.status_code)
        res = pc.get('/program/upload/?result=failed')
        self.assertEqual(200, res.status_code)
    def test_ajax_upload(self):
        pg = ProgramGroup(title='upload_group')
        pg.save()
        ps = ProgramSeries(title='upload_sereis')
        ps.save()
        pc = PoweredClient('worker')
        res = pc.post('/program/upload/ajaxupload/',
                      {'group': 0})
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/program/upload/ajaxupload/',
                      {'group': -1})
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/program/upload/ajaxupload/',
                      {'group': pg.id, 'series': ps.id, 'title': 'uploaded',
                       'description': 'description', 'weight': 0,
                       'recorder': 'recorder', 'workers': 'workers',
                       'contributor': 'contributor'})
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/program/upload/ajaxupload/',
                      {'group': pg.id, 'series': ps.id, 'title': 'uploaded',
                       'description': 'description', 'weight': 0,
                       'recorder': 'recorder', 'workers': 'workers',
                       'contributor': 'contributor', })
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/program/upload/ajaxupload/',
                      {'group': pg.id, 'series': ps.id, 'title': 'uploaded',
                       'description': 'description', 'weight': 0,
                       'recorder': 'recorder', 'workers': 'workers',
                       'contributor': 'contributor',
                       'picture': open('static/images/1.jpg'),
                       'audio': open('static/js/csrfajax.js'),
                       'document': open('static/js/csrfajax.js'), })
        self.assertEqual(True, json.loads(res.content)['success'])
    def test_show_modify(self):
        pro = Program.objects.filter(audio__gt=0, series_id__gt=0)[0]
        pc = PoweredClient('worker')
        res = pc.get('/program/modify/' + str(pro.id))
        self.assertEqual(200, res.status_code)
    def test_modify_program(self):
        pro = Program.objects.filter(audio__gt=0, series_id__gt=0)[0]
        pc = PoweredClient('worker')
        res = pc.post('/program/modify_program/' + str(pro.id) + '/',
                      {'group': pro.group.id, 'series': pro.series.id, 'title': 'uploaded',
                       'description': 'description', 'weight': 0,
                       'recorder': 'recorder', 'workers': 'workers',
                       'contributor': 'contributor',
                       'picture': open('static/images/1.jpg'),
                       'audio': open('static/js/csrfajax.js'),
                       'document': open('static/js/csrfajax.js'), })
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/program/modify_program/' + str(pro.id) + '/',
                      {'group': '0'})
        self.assertEqual(False, json.loads(res.content)['success'])
        res = pc.post('/program/modify_program/' + str(pro.id) + '/',
                      {'group': '-1'})
        self.assertEqual(False, json.loads(res.content)['success'])
        pro2 = Program(title='no_uploader')
        pro2.save()
        res = pc.post('/program/modify_program/' + str(pro2.id) + '/')
        self.assertEqual(False, json.loads(res.content)['success'])
    def test_del_program(self):
        pro = Program(title="comment_program")
        pro.save()
        pc = PoweredClient('admin')
        res = pc.post('/program/delete/', {'pid': pro.id, })
        self.assertEqual(True, json.loads(res.content)['success'])
        res = pc.post('/program/delete/', {'pid': 99999, })
        self.assertEqual(False, json.loads(res.content)['success'])

    def test_recommand_program(self):
        pro = Program(title='recommanded')
        pro.save()
        pc = PoweredClient('worker')
        res = pc.post('/program/recommand/',
                      {'id': pro.id, 'weight': 1})
        self.assertTrue('forbidden' in res.content)
        pc = PoweredClient('admin')
        res = pc.post('/program/recommand/',
                      {'id': pro.id, 'weight': 1})
        self.assertEqual(True, json.loads(res.content)['success'])




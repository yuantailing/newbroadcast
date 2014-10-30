# -*- coding: UTF-8 -*-
import unittest
import random
from models import *

class ModelsTest(unittest.TestCase):
    def test_user_normal_use(self):
        s = str(random.random())
        user = User()
        user.email = s
        user.nickname = s
        user.password = '123456'
        user.save
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

def run_test():
    suite_models = unittest.TestLoader().loadTestsFromTestCase(ModelsTest)
    suite = unittest.TestSuite([suite_models])
    unittest.TextTestRunner().run(suite)

if __name__ =='__main__':
    print 'You must run test in manage.py shell'
    run_test()

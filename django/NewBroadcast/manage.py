# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers

from models import *
import json

def power_trans(power_str):
    power_dic = {'user':u'普通用户',
                 'worker':u'台员',
                 'admin':u'管理员',
                 'superadmin':u'超级管理员',
                 }
    if power_str in power_dic:
        return power_dic[power_str]
    else:
        return u'未知权限'

@power_required(['user'])
def show_space(req):
    user = User.objects.get(id=req.session['uid'])
    ups = Program.objects.filter(uploader=user).order_by('-create_time')[0:5]
    favs = Program.objects.filter(favorite__in=user.favorite.all())
    return render_to_response("manage/space.html",
                              {'user':user,
                               'power':power_trans(user.power),
                               'ups':ups,
                               'favs':favs, },
                              context_instance=RequestContext(req));

@power_required(['user'])
def show_favorites(req):
    user = User.objects.get(id=req.session['uid'])
    favs = Program.objects.filter(favorite__in=user.favorite.all())
    return render_to_response("manage/favorites.html",
                              {'user':user,
                               'obj_list':favs, },
                              context_instance=RequestContext(req));

@power_required(['user'])
def show_favorites_table(req):
    user = User.objects.get(id=req.session['uid'])
    favs = Program.objects.filter(favorite__in=user.favorite.all())
    return render_to_response("manage/myresource.html",
                              {'title':u'我的收藏',
                               'obj_list':favs, },
                              context_instance=RequestContext(req))

@power_required(['worker'])
def show_mgrres(req):
    return render_to_response("manage/resource.html",
                              context_instance=RequestContext(req))

@power_required(['worker'])
def show_mgrmyres(req):
    obj_list = Program.objects.filter(uploader__id=req.session['uid'])
    return render_to_response("manage/myresource.html",
                              {'title':u'我的上传',
                               'obj_list':obj_list, },
                              context_instance=RequestContext(req))

@power_required(['admin'])
def show_mgrallres(req):
    obj_list = Program.objects.all()
    return render_to_response("manage/myresource.html",
                              {'title':u'所有上传',
                               'obj_list':obj_list, },
                              context_instance=RequestContext(req))

@power_required(['superadmin'])
def show_mgruser(req):
    obj_list = User.objects.all()
    if req.REQUEST.get('wd', None):
        search = req.REQUEST.get('wd', None)
        g1 = obj_list.filter(email__contains=search)
        g2 = obj_list.filter(nickname__contains=search)
        g3 = obj_list.filter(power__contains=search)
        g4 = obj_list.filter(birthday__contains=search)
        g5 = obj_list.filter(phone_number__contains=search)
        obj_list = g1 | g2 | g3 | g4 | g5
    return render_to_response("manage/user.html",
                              {'obj_list':obj_list, },
                              context_instance=RequestContext(req))

@power_required(['user'])
def change_password(req):
    res = {}
    psw_old = req.POST.get('old_password', None)
    psw0 = req.POST.get('new_password', None)
    psw1 = req.POST.get('check_password', None)
    if psw0 and psw0 == psw1:
        user = User.objects.get(id=req.session['uid'])
        if user.password == psw_old:
            user.password = psw0
            user.save()
            res['success'] = True
            res['info'] = u'修改密码成功'
        else:
            res['success'] = False
            res['info'] = u'旧密码错误'
    else:
        res['success'] = False
        res['info'] = u'密码不一致'
    return HttpResponse(json.dumps(res), content_type='application/json')

@power_required(['user'])
def change_info(req):
    res = {}
    nick = req.POST.get('nickname', None)
    birth = req.POST.get('birth', None)
    phone = req.POST.get('phone', None)
    try:
        try:
            user = User.objects.get(nickname=nick)
            if user.id == req.session['uid']:
                raise Exception
            res['success'] = False
            res['info'] = u'昵称已存在'
        except Exception, e:
            user = User.objects.get(id=req.session['uid'])
            if nick:
                if '@' in nick:
                    res['success'] = False
                    res['info'] = u'昵称不能含@字符'
                    return HttpResponse(json.dumps(res),
                                        content_type='application/json')
                else:
                    user.nickname = nick
            user.birthday = birth
            user.phone_number = phone
            if not birth:
                user.birthday = None
            if not phone:
                user.phone_number = None
            user.save()
            res['success'] = True
            res['info'] = u'修改资料成功'
    except Exception, e:
        res['success'] = False
        res['info'] = u'日期格式错误'
    return HttpResponse(json.dumps(res), content_type='application/json')

@power_required(['superadmin'])
def change_power(req):
    res = {}
    try:
        new_user = User.objects.get(id=int(req.POST.get('uid', None)))
        new_power = req.POST.get('new_power', None)
        if new_user.id == req.session['uid']:
            return HttpResponse(json.dumps({'success':False, 'info':'不能修改自己的权限'}),
                                content_type='application/json')
        else:
            if not new_power in ['user', 'worker', 'admin', 'superadmin']:
                return HttpResponse(json.dumps({'success':False, 'info':'权限的选择有误'}),
                                    content_type='application/json')
            else:
                new_user.power = new_power
                new_user.save()
                return HttpResponse(json.dumps({'success':True, 'info':'修改成功'}),
                                    content_type='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({'success':False, 'info':'未知错误'}),
                            content_type='application/json')


@power_required(['superadmin'])
def groupseries(req):
    return render_to_response("manage/groupseries.html",
                              context_instance=RequestContext(req))


def group_series_post(model, req):
    try:
        obj = model.objects.get(id=req.REQUEST.get('id', None))
    except Exception, e:
        obj = None
    new_name = req.REQUEST.get('new_name', None)
    if req.REQUEST.get('action', None) == 'modify':
        if not obj:
            return HttpResponse(json.dumps({'success':False, 'info':'目标不存在'}),
                                content_type='application/json')
        if not new_name:
            return HttpResponse(json.dumps({'success':False, 'info':'名称不能为空'}),
                                content_type='application/json')
        obj.title = new_name
        obj.save()
        return HttpResponse(json.dumps({'success':True, 'info':'修改成功'}),
                            content_type='application/json')
    if req.REQUEST.get('action', None) == 'delete':
        if not obj:
            return HttpResponse(json.dumps({'success':False, 'info':'目标不存在'}),
                                content_type='application/json')
        obj.order = -1
        obj.save()
        return HttpResponse(json.dumps({'success':True, 'info':'删除成功'}),
                            content_type='application/json')
    if req.REQUEST.get('action', None) == 'destroy':
        if not obj:
            return HttpResponse(json.dumps({'success':False, 'info':'目标不存在'}),
                                content_type='application/json')
        if obj.program.count() > 0:
            return HttpResponse(json.dumps({'success':False, 'info':'只有节目数量为0才能删除'}),
                                content_type='application/json')
        obj.delete()
        return HttpResponse(json.dumps({'success':True, 'info':'删除成功'}),
                            content_type='application/json')
    if req.REQUEST.get('action', None) == 'restore':
        if not obj:
            return HttpResponse(json.dumps({'success':False, 'info':'目标不存在'}),
                                content_type='application/json')
        obj.order = 0
        obj.save()
        return HttpResponse(json.dumps({'success':True, 'info':'恢复成功'}),
                            content_type='application/json')
    if req.REQUEST.get('action', None) == 'add':
        if not new_name:
            return HttpResponse(json.dumps({'success':False, 'info':'名称不能为空'}),
                                content_type='application/json')
        model(title=new_name).save()
        return HttpResponse(json.dumps({'success':True, 'info':'创建成功'}),
                            content_type='application/json')
    if req.REQUEST.get('action', None) == 'sort':
        try:
            new_order = req.REQUEST.getlist('new_order[]')
            new_order = list(int(a) for a in new_order)
            abled = model.objects.filter(order__gte=0)
            if abled.count() == len(new_order):
                for obj in abled:
                    obj.order = len(new_order) - new_order.index(obj.id)
                for obj in abled:
                    obj.save()
            else:
                raise Exception
        except Exception, e:
            return HttpResponse(json.dumps({'success':False, 'info':'序列错误'}),
                    content_type='application/json')
        return HttpResponse(json.dumps({'success':True, 'info':'排序成功'}),
                            content_type='application/json')
    return None

@power_required(['superadmin'])
def program_group(req):
    hr = group_series_post(ProgramGroup, req)
    if hr:
        return hr
    obj_list = ProgramGroup.objects.all(),
    return render_to_response("manage/groupiframe.html",
                              {'title':u'组别',
                               'obj_type':'group',
                               'obj_list':ProgramGroup.objects.filter(order__gte=0).order_by('-order'),
                               'removed_list':ProgramGroup.objects.filter(order__lt=0), },
                              context_instance=RequestContext(req))

@power_required(['superadmin'])
def program_series(req):
    hr = group_series_post(ProgramSeries, req)
    if hr:
        return hr
    return render_to_response("manage/groupiframe.html",
                              {'title':u'系列',
                               'obj_type':'series',
                               'obj_list':ProgramSeries.objects.filter(order__gte=0).order_by('-order'),
                               'removed_list':ProgramSeries.objects.filter(order__lt=0), },
                              context_instance=RequestContext(req))


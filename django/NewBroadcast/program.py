# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import *
from django import template
from django.template.loader import get_template
from django.db import models
from django.core import serializers
from django import forms
import json
import os
import re
from models import *

@power_required([None])
def show_program(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id=pgid)

    description = ""
    if pg.description:
        description = pg.description

    table = []
    if pg.group:
        table.append((u"节目组别", pg.group.title))
    if pg.series:
        table.append((u"节目系列", pg.series.title))
    if pg.recorder:
        table.append((u"录音/播音人员名单", pg.recorder))
    if pg.contributor:
        table.append((u"稿件来源", pg.contributor))
    if pg.workers:
        table.append((u"机务人员", pg.workers))

    piclink = []
    if pg.picture:
        pic_arr = json.loads(pg.picture)
        for i in pic_arr:
            s = Source.objects.get(id=i)
            if s.thumb:
                piclink.append(s.thumb.url)
            else:
                piclink.append(s.document.url)
    
    medialink = ""
    if pg.audio:
        medialink = Source.objects.get(id=pg.audio).document.url

    doc_links = []
    if pg.document:
        doc_arr = json.loads(pg.document)
        for i in range(0, len(doc_arr)):
            src = Source.objects.get(id=doc_arr[i])
            if i == 0:
                doc_links.append((u"稿件下载", src.document.url, u"稿件" + str(i + 1)
                                  + u" 下载链接"))
            else:
                doc_links.append((u"", src.document.url, u"稿件" + str(i + 1)
                                  + u" 下载链接"))

    have_praised = False
    have_favorited = False
    try:
        user = User.objects.get(id=req.session['uid'])
        have_praised = Praise.objects.filter(user=user, program=pg).count() > 0
        have_favorited = Favorite.objects.filter(user=user, program=pg).count() > 0
    except Exception, e:
        user = None

    return render_to_response("program/show.html",
                    {'pgid':pgid, 'title':pg.title,
                     'strong':description[0:1], 'description':description[1:],
                     'medialink':medialink, 'piclink':piclink,
                     'table':table, 'doc_links':doc_links,
                     'praise_count': pg.praise.count(),
                     'favorite_count': pg.favorite.count(),
                     'logined':not (user == None),
                     'have_praised':have_praised,
                     'have_favorited':have_favorited,
                     'comments':pg.comment.order_by('-create_time'), },
                    context_instance=RequestContext(req));

@power_required([None])
def play_program(req, arg):
    return render_to_response("program/player.html",
                              context_instance=RequestContext(req));

def add_user_program_only_item(OnlyClassName, req):
    try:
        user = User.objects.get(id=req.session['uid'])
        pg = Program.objects.get(id=req.REQUEST.get('pid'))
        OnlyClassName(user=user, program=pg).save()
        return HttpResponse(json.dumps({'success':True, 'info':'success',
                                        'count':OnlyClassName.objects.filter(program__id=pg.id).count()}),
                            content_type='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({'success':False, 'info':'repeated'}),
                            content_type='application/json')

def del_user_program_item(OnlyClassName, req):
    try:
        pid = req.REQUEST.get('pid')
        pr = OnlyClassName.objects.filter(user__id=req.session['uid'],
                                   program__id=req.REQUEST.get('pid'))
        pr.delete()
        return HttpResponse(json.dumps({'success':True, 'info':'success',
                                        'count':OnlyClassName.objects.filter(program__id=pid).count()}),
                            content_type='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({'success':False, 'info':'not found'}),
                            content_type='application/json')

@power_required(['user'])
def praise(req):
    return add_user_program_only_item(Praise, req)

@power_required(['user'])
def un_praise(req):
    return del_user_program_item(Praise, req)

@power_required(['user'])
def favorite(req):
    return add_user_program_only_item(Favorite, req)

@power_required(['user'])
def un_favorite(req):
    return del_user_program_item(Favorite, req)

@power_required(['user'])
def add_comment(req):
    user = User.objects.get(id=req.session['uid'])
    pg = Program.objects.get(id=req.REQUEST.get('pid'))
    comment = req.REQUEST.get('comment')
    if len(comment) < 5:
        return HttpResponse(json.dumps({'success':False, 'info':'评论不能少于5个字'}),
                            content_type='application/json')
    Comment(user=user, program=pg, content=comment).save()
    return HttpResponse(json.dumps({'success':True, 'info':'评论成功'}),
                        content_type='application/json')

@power_required(['superadmin'])
def del_comment(req):
    user = User.objects.get(id=req.session['uid'])
    try:
        cm = Comment.objects.get(id=req.REQUEST.get('cid'))
        cm.delete()
        return HttpResponse(json.dumps({'success':True, 'info':'success'}),
                            content_type='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({'success':False, 'info':'not found'}),
                            content_type='application/json')

@power_required(['worker'])
def show_upload(req):
    result = req.GET.get('result', None)
    if result == 'success':
        result = u'上传成功'
    elif result == 'failed':
        result = u'操作失败'

    group_all = ProgramGroup.objects.filter(order__gte=0).order_by('-order')
    series_all = ProgramSeries.objects.filter(order__gte=0).order_by('-order')
    
    return render_to_response("program/upload.html",
                              {'result':result,
                               'group_all':group_all,
                               'series_all':series_all},
                              context_instance=RequestContext(req))


@power_required(['worker'])
def ajax_upload(req):
    try:
        prg = Program()
        
        tgroup = req.POST.get('group', None)
        tseries = req.POST.get('series', None)
        ttitle = req.POST.get('title', None)
        tdescription = req.POST.get('description', None)
        tweight = req.POST.get('weight', None)
        trecorder = req.POST.get('recorder', None)
        tworkers = req.POST.get('workers', None)
        tcontributor = req.POST.get('contributor', None)
        tpicture = req.FILES.getlist('picture', None) # json of list
        taudio = req.FILES.get('audio', None)
        tdocument = req.FILES.getlist('document', None) # json of list
        user = User.objects.get(id=req.session['uid'])
        if (tgroup == "0"):
            return HttpResponse(json.dumps({'success':False, 'info':'组别不能为空!'}),
                        content_type='application/json')
        else:
            pgroup = ProgramGroup.objects.get(id = int(tgroup))
            prg.group = pgroup
        if (tseries != "0"):
            pseries = ProgramSeries.objects.get(id = int(tseries))
            prg.series = pseries
        if (ttitle == None or ttitle == ''):
            return HttpResponse(json.dumps({'success':False, 'info':'标题不能为空!'}),
                        content_type='application/json')
        else:
            prg.title = ttitle
        if (tdescription != None):
            prg.description = tdescription
        if (tweight != None):
            prg.weight = tweight
        if (trecorder != None):
            prg.recorder = trecorder
        if (tworkers != None):
            prg.workers = tworkers
        if (tcontributor != None):
            prg.contributor = tcontributor
        if (tpicture != None):
            pics = []
            for ele in tpicture:
                pic = Source()
                pic.document = ele
                pic.save()
                pics.append(pic.id)
            prg.picture = json.dumps(pics)
        if (taudio != None):
            ad = Source()
            ad.document = taudio
            ad.save()
            prg.audio = ad.id
        if (tdocument != None):
            docs = []
            for ele in tdocument:
                doc = Source()
                doc.document = ele
                doc.save()
                docs.append(doc.id)
            prg.document = json.dumps(docs)
        if (user != None):
            prg.uploader = user
        prg.save()
        success = True
    except Exception, e:
        success = False
    return HttpResponse(json.dumps({'success':success, 'info':'上传失败，请检查输入！'}),
                        content_type='application/json')


@power_required(['worker'])
def show_modify(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id=pgid)

    
    group_all = ProgramGroup.objects.filter(order__gte=0).order_by('-order')
    series_all = ProgramSeries.objects.filter(order__gte=0).order_by('-order')

    group = 0
    if pg.group:
        group = pg.group.id
    series = 0
    if pg.series:
        series = pg.series.id
    title = ""
    if pg.title:
        title = pg.title
    description = ""
    if pg.description:
        description = pg.description
    recorder = ""
    if pg.recorder:
        recorder = pg.recorder
    contributor = ""
    if pg.contributor:
        contributor = pg.contributor
    workers = ""
    if pg.workers:
        workers = pg.workers

    pictitle = []
    if pg.picture:
        pic_arr = json.loads(pg.picture)
        for i in pic_arr:
            pic = {}
            try:
                pic['title'] = os.path.split(Source.objects.get(id=i).document.file.name)[1]
            except Exception, e:
                pic['title'] = "此文件已被删除，请手动删除该条目"
            pic['id'] = i
            pictitle.append(pic)

    mediatitle = ""
    if pg.audio:
        try:
            mediatitle = os.path.split(Source.objects.get(id=pg.audio).document.file.name)[1]
        except Exception, e:
            mediatitle = "此文件已被删除，请手动删除该条目"

    doctitle = []
    if pg.document:
        doc_arr = json.loads(pg.document)
        for i in doc_arr:
            doc = {}
            try:
                doc['title'] = os.path.split(Source.objects.get(id=i).document.file.name)[1]
            except Exception, e:
                doc['title'] = "此文件已被删除，请手动删除该条目"
            doc['id'] = i
            doctitle.append(doc)

    return render_to_response("program/modify.html",
                    {'pgid':pgid, 'group':group,
                     'series':series, 'title':title,
                     'description':description, 'recorder':recorder,
                     'contributor':contributor, 'workers':workers,
                     'mediatitle':mediatitle, 'pictitle':pictitle,
                     'doctitle':doctitle, 'groups':group_all,
                     'series_all':series_all},
                     context_instance=RequestContext(req));

@power_required(['worker'])
def modify_program(req, arg):
    pgid = int(arg)
    pg = Program.objects.get(id=pgid)

    try:
        res = { }
        user = User.objects.get(id=req.session['uid'])
        if (user.power == 'worker') and (not pg.uploader or not user.id == pg.uploader.id):
            return HttpResponse(json.dumps({'success':False, 'info':'您只能修改自己上传的文件！'}),
                        content_type='application/json')
        tgroup = req.POST.get('group', None)
        tseries = req.POST.get('series', None)
        ttitle = req.POST.get('title', None)
        tdescription = req.POST.get('description', None)
        trecorder = req.POST.get('recorder', None)
        tcontributor = req.POST.get('contributor', None)
        tworkers = req.POST.get('workers', None)
        if (tgroup == "0"):
            return HttpResponse(json.dumps({'success':False, 'info':'组别不能为空！'}),
                        content_type='application/json')
        else:
            group = ProgramGroup.objects.get(id = int(tgroup))
            pg.group = group
        if tseries != "0":
            series = ProgramSeries.objects.get(id = int(tseries))
            pg.series = series
        else:
            pg.series = None
        if not ttitle:
            return HttpResponse(json.dumps({'success':False, 'info':'标题不能为空!'}),
                        content_type='application/json')
        else:
            pg.title = ttitle
        if (tdescription != None):
            pg.description = tdescription
        if (trecorder != None):
            pg.recorder = trecorder
        if (tcontributor != None):
            pg.contributor = tcontributor
        if (tworkers != None):
            pg.workers = tworkers
        taudio = req.FILES.get('audio', None)
        if (taudio != None):
            ad = Source()
            ad.document = taudio
            ad.save()
            pg.audio = ad.id
        pic_arr = json.loads(pg.picture)
        tpic = req.FILES.getlist('picture', None)
        if (len(tpic) > 0):
            for ele in tpic:
                pic = Source()
                pic.document = ele
                pic.save()
                pic_arr.append(pic.id)
        pg.picture = json.dumps(pic_arr)
        doc_arr = json.loads(pg.document)
        
        tdoc = req.FILES.getlist('document', None)
        if (len(tdoc) > 0):
            for ele in tdoc:
                doc = Source()
                doc.document = ele
                doc.save()
                doc_arr.append(doc.id)
        pg.document = json.dumps(doc_arr)
        pg.save()
        success = True
    except Exception, e:
        success = False
    return HttpResponse(json.dumps({'success':success, 'info':'上传失败，请检查输入！'}),
                        content_type='application/json')


@power_required(['worker'])
def del_pic(req):
    prgid = req.REQUEST.get('prgid', None)
    pg = Program.objects.get(id=prgid)
    user = User.objects.get(id=req.session['uid'])
    if user.power == 'worker' and (not pg.uploader or user.id != pg.uploader.id):
        return HttpResponse(json.dumps({'success':False, 'info':'您只能修改自己上传的文件！'}),
                        content_type='application/json')
    picid = req.REQUEST.get('picid', None)
    pg = Program.objects.get(id=prgid)
    pic_arr = json.loads(pg.picture)
    try:
        pic_arr.remove(int(picid))
        pg.picture = json.dumps(pic_arr)
        pg.save()
        success = True
    except Exception, e:
        success = False
    return HttpResponse(json.dumps({'success':success, 'info':'删除失败，请重新尝试！'}), content_type='application/json')

@power_required(['worker'])
def del_doc(req):
    prgid = req.REQUEST.get('prgid', None)
    pg = Program.objects.get(id=prgid)
    user = User.objects.get(id=req.session['uid'])
    if user.power == 'worker' and (not pg.uploader or user.id != pg.uploader.id):
        return HttpResponse(json.dumps({'success':False, 'info':'您只能修改自己上传的文件！'}),
                        content_type='application/json')
    docid = req.REQUEST.get('docid', None)
    pg = Program.objects.get(id=prgid)
    doc_arr = json.loads(pg.document)
    try:
        doc_arr.remove(int(docid))
        pg.document = json.dumps(doc_arr)
        pg.save()
        success = True
    except Exception, e:
        success = False
    return HttpResponse(json.dumps({'success':success, 'info':'删除失败，请重新尝试！'}), content_type='application/json')

@power_required(['worker'])
def delete_program(req):
    try:
        pid = req.REQUEST.get('pid', None)
        pg = Program.objects.get(id=pid)
        pg.delete()
        return HttpResponse(json.dumps({'success':True}),
                            content_type='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({'success':False}),
                            content_type='application/json')
    
@power_required(['admin'])
def recommand_program(req):
    p_id = req.POST.get('id');
    p_weight = req.POST.get('weight');
    obj = Program.objects.get(id = p_id);
    obj.weight = p_weight;
    return HttpResponse(json.dumps({"success": True}),
                        content_type = "application/json");

@power_required(['user'])
def get_all_favorites(req):
    uid = req.session['uid'];
    fav = Favorite.objects.filter(user__id=uid);
    print fav;
    pgs = Program.objects.filter(favorite__in=fav).exclude(audio=None).order_by('favorite');
    res = [];
    for pg in pgs:
        tmp = {}
        tmp['id'] = pg.id;
        tmp['title'] = pg.title;
        tmp['url'] = Source.objects.get(id=pg.audio).document.url;
        tmp['description'] = None;
        tmp['have_praised'] = False;
        tmp['have_favorited'] = False;
        tmp['praise_count'] = pg.praise.count();
        tmp['favorite_count'] = pg.favorite.count();
        if pg.picture:
            pic_arr = json.loads(pg.picture)
            for i in pic_arr:
                s = Source.objects.get(id=i)
                if s.thumb:
                    tmp['thumbnail'] = s.thumb.url;
                else:
                    tmp['thumbnail'] = s.document.url;
                break;
        else:
            tmp['thumbnail'] = None;
        tmp['have_praised'] = Praise.objects.filter(user__id=uid, program=pg).count() > 0
        tmp['have_favorited'] = Favorite.objects.filter(user__id=uid, program=pg).count() > 0
        if (pg.description):
            tmp['description'] = pg.description
        res.append(tmp);
    print res;
    return HttpResponse(json.dumps(res), content_type = "application/json");
    
@power_required([None])
def get(req):
    pg = Program.objects.get(id=req.GET.get('pid'))
    res = {}
    res['id'] = pg.id;
    res['title'] = pg.title;
    res['description'] = None;
    res['piclink'] = None;
    res['medialink'] = None;
    if pg.description:
        res['description'] = pg.description;
    if pg.audio:
        res['medialink'] = Source.objects.get(id=pg.audio).document.url
    if not (pg.picture == '[]' or not pg.picture):
        pic_arr = json.loads(pg.picture)
        s = Source.objects.get(id=pic_arr[0])
        if s.thumb:
            res['piclink'] = s.thumb.url
        else:
            res['piclink'] = s.document.url
    return HttpResponse(json.dumps({'program':res}), content_type='application/json')

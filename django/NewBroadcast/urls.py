from django.conf.urls import patterns, include, url
from django.contrib import admin
from NewBroadcast import frontpage
from NewBroadcast import resource
from NewBroadcast import program
from NewBroadcast import login
from NewBroadcast import manage


urlpatterns = patterns(
    '',
    
    url(r'^$', frontpage.show_index),
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'upload/'}),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^index/$', frontpage.show_index),
    url(r'^index/waterflow$', frontpage.waterflow_data),

    url(r'^resource/$', resource.show),
    url(r'^resource/sort/$', resource.sort),
    url(r'^resource/filter/$', resource.filter),
    url(r'^resource/listall/$', resource.list_all),
    url(r'^resource/groupfilter/([0-9]+)$', resource.group_filter),
    url(r'^resource/getarr/$', resource.get_arr),

    url(r'^program/([0-9]+)$', program.show_program),
    url(r'^program/play/(.*)$', program.play_program),
    url(r'^program/praise/$', program.praise),
    url(r'^program/unpraise/$', program.un_praise),
    url(r'^program/favorite/$', program.favorite),
    url(r'^program/unfavorite/$', program.un_favorite),
    url(r'^program/comment/add/', program.add_comment),
    url(r'^program/comment/del/', program.del_comment),
    url(r'^program/upload/ajaxupload/$', program.ajax_upload),
    url(r'^program/upload/$', program.show_upload),
    url(r'^program/modify/([0-9]+)$', program.show_modify),
    url(r'^program/modify_program/([0-9]+)/$', program.modify_program),
    url(r'^program/modify/delpic/$', program.del_pic),
    url(r'^program/modify/deldoc/$', program.del_doc),
    url(r'^program/delete/$', program.delete_program),
    url(r'^program/get_all_favorites$', program.get_all_favorites),
    url(r'^program/get/$', program.get),
    url(r'^program/recommand/$', program.recommand_program),

    url(r'^login/do/$', login.login),
    url(r'^login/test/$', login.test),
    url(r'^login/logout/$', login.logout),
    url(r'^signin/judge/$', login.exist_judge),
    url(r'^signin/do/$', login.signin),

    url(r'^space/$', manage.show_space),
    url(r'^manage/favorites/$', manage.show_favorites),
    url(r'^manage/resource/$', manage.show_mgrres),
    url(r'^manage/myresource/$', manage.show_mgrmyres),
    url(r'^manage/allresources/$', manage.show_mgrallres),
    url(r'^manage/user/$', manage.show_mgruser),
    url(r'^manage/changepassword/$', manage.change_password),
    url(r'^manage/changeinfo/$', manage.change_info),
    url(r'^manage/changepower/$', manage.change_power),
    url(r'^manage/groupseries/$', manage.groupseries),
    url(r'^manage/groupseries/group/$', manage.program_group),
    url(r'^manage/groupseries/series/$', manage.program_series),

)

from django.conf import settings
if settings.DEBUG is False:  # if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT,
                                 }),
                            )

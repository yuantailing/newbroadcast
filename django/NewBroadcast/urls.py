from django.conf.urls import patterns, include, url
from django.contrib import admin
from NewBroadcast import ajaxtest
from NewBroadcast import frontpage
from NewBroadcast import resource
from NewBroadcast import program
from NewBroadcast import login
from NewBroadcast import signin
from NewBroadcast import api
from NewBroadcast import manager


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NewBroadcast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', frontpage.show_index),
    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'upload/'}),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ajaxtest/$', ajaxtest.index),
    url(r'^ajaxtest/getresult/$', ajaxtest.getresult),

    url(r'^index/$', frontpage.show_index),
    url(r'^index/waterflow$', frontpage.waterflow_data),

    url(r'^resource/$', resource.show),
    url(r'^resource/listall/$', resource.list_all),
    url(r'^resource/groupfilter/([0-9]*)$', resource.group_filter),
    url(r'^resource/getarr/$', resource.get_arr),
    url(r'^resource/getarr_test/$', resource.getarr_test),
    url(r'^resource/result/$', resource.result),

    url(r'^program/([0-9]*)$', program.show_program),
    url(r'^program/play/(.*)$', program.play_program),
    url(r'^program/upload/$', program.show_upload),
    url(r'^program/upload/dealupload/$', program.upload_program),

    url(r'^login/do/$', login.do),
    url(r'^login/test/$', login.test),
    url(r'^login/logout/$', login.logout),

    url(r'^signin/judge/$', signin.judge),
    url(r'^signin/do/$', signin.do),

    url(r'^user/$', api.api_user),
    url(r'^program_group/$', api.api_program_group),
    url(r'^program_series/$', api.api_program_series),
    url(r'^program/$', api.api_program),
    url(r'^api_source/$', api.api_source),
    url(r'^api_comment/$', api.api_comment),

    url(r'^space/$', manager.show_space),
    url(r'^mgrres/$', manager.show_mgrres),
    url(r'^mgruser/$', manager.show_mgruser),

)

from django.conf import settings
if settings.DEBUG is False: #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
                            url(r'^static/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.STATIC_ROOT,
                                 }),
                            )

from django.conf.urls import patterns, include, url
from django.contrib import admin
from NewBroadcast import frametest
from NewBroadcast import signin
from NewBroadcast import ajaxtest
from NewBroadcast import api
from NewBroadcast import test


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NewBroadcast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'upload/'}),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', frametest.ctime),
    url(r'^hello/(.+)/', frametest.hello),
    url(r'^temp/', frametest.temp),

    url(r'^ajaxtest/$', ajaxtest.index),
    url(r'^ajaxtest/getresult/$', ajaxtest.getresult),

    url(r'^signin$', signin.Signin.form),
    url(r'^signin/do$', signin.Signin.do),
	
	url(r'^user/$', api.api_user),
	url(r'^program_group/$', api.api_program_group),
	url(r'^program_series/$', api.api_program_series),
	url(r'^program/$', api.api_program),
	url(r'^api_source/$', api.api_source),
	url(r'^api_comment/$', api.api_comment),

	url(r'^user_test/$', test.test_user),

)

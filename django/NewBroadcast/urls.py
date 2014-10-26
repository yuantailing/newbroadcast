from django.conf.urls import patterns, include, url
from django.contrib import admin
from NewBroadcast import frametest
from NewBroadcast import signin
from NewBroadcast import ajaxtest


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

)

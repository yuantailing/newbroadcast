from django.conf.urls import patterns, include, url
from django.contrib import admin
from frametest import hello, ctime, temp
from signin import Signin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NewBroadcast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'upload/'}),

    url(r'^$', ctime),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/(.+)/', hello),
    url(r'^temp/', temp),

    url(r'^signin$', Signin.form),
    url(r'^signin/do$', Signin.do),

)

from django.conf.urls import patterns, include, url
from django.contrib import admin
from frametest import hello, ctime, temp

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NewBroadcast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', ctime),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello/(.+)/', hello),
    url(r'^temp/', temp),
)

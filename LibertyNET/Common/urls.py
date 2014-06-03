from django.conf.urls import patterns, url
from Common.views import register, user_login, logout

urlpatterns = patterns('',
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    )

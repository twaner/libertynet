from django.conf.urls import patterns, url
from Common.views import register

urlpatterns = patterns('',
    url(r'^register/$', register, name='register'),
    )

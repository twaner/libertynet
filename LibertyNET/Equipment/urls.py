from django.conf.urls import patterns, include, url
from django.contrib import admin
from Equipment.views import CreateInventoryPart, PartIndex

urlpatterns = patterns('',
                       url(r'^index/$', PartIndex.as_view(), name='index'),
                       url(r'^addpart/$', CreateInventoryPart.as_view(), name="addpart"),

)

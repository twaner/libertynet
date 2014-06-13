from django.conf.urls import patterns, include, url
from django.contrib import admin
from Equipment.views import CreateInventoryPart

urlpatterns = patterns('',
                       url(r'^addpart/$', CreateInventoryPart.as_view(), name="addpart"),

)

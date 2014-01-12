from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from models import Client, Sales_Prospect

client_info = {
    'queryset': Client.objects.all(),
    'template_name': 'index.html',
    'template_object_name': 'client',
}

urlpatterns = patterns('',
     (r'^index1/$', direct_to_template, {
        'template': 'index1.html'
    }),
    (r'^index/$', list_detail.object_list, client_info)
)

from django.conf.urls import patterns, include, url
from views import ClientDetailList, ClientListView

urlpatterns = patterns('',
    url(r'index/$', ClientListView.as_view(), name='index'),
    #url(r'employee/([\d-]+)/$', EmployeeDetailList.as_view() name='details),

)

"""
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
"""
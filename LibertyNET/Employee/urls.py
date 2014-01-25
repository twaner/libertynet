from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import EmployeeListView, EmployeeDetailList, addemployee, EmployeeDetailView, editemployee
#region urlpatterns


urlpatterns = patterns('',
    url(r'^index/$', EmployeeListView.as_view(), name="index"),
    url(r'addemployee/$', addemployee, name='addemployee'),
    url(r'^(?P<pk>[\d-]+)/$', EmployeeDetailView.as_view(), name='details'),
    url(r'editemployee/(?P<employee_id>\d+)/$', editemployee, name='editemployee'),
    #url(r'employee/(?P<pk>[\d-]+)/$', EmployeeDetailList.as_view(), name='details'),
    #url(r'employee/([\d-]+)/$', EmployeeDetailList.as_view(), name='details'),
)

#endregion

"""
#region generic views


employee_info = {
    'queryset': Employee.objects.all(),
    'template_name': 'index.html',
    'template_object_name': 'all_employees',
}

urlpatterns = patterns('',
    (r'^employee/$', list_detail.object_list, employee_info),

)
#endregion
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import EmployeeListView, EmployeeDetailList
#region urlpatterns


urlpatterns = patterns('',
    url(r'^index/$', EmployeeListView.as_view(), name="index"),
    #url(r'employee/([\d-]+)/$', EmployeeDetailList.as_view()),
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
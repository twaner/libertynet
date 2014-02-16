from django.conf.urls import patterns, include, url
from django.contrib import admin
from Employee.views import EmployeeListView, addemployee, EmployeeDetailView, editemployee

#region urlpatterns

urlpatterns = patterns('',
    url(r'^index/$', EmployeeListView.as_view(), name="index"),
    url(r'addemployee/$', addemployee, name='addemployee'),
    url(r'^(?P<pk>[\d-]+)/$', EmployeeDetailView.as_view(), name='details'),
    url(r'editemployee/(?P<pk>\d+)/$', editemployee, name='editemployee'),
    #url(r'employee/(?P<pk>[\d-]+)/$', EmployeeDetailList.as_view(), name='details'),
    #url(r'employee/([\d-]+)/$', EmployeeDetailList.as_view(), name='details'),
)

#endregion


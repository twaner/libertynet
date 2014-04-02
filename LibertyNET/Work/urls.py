from django.conf.urls import patterns, url
from Work.views import JobView, JobDetailView, JobListView, TaskDetailView, TaskListView, TaskView, \
    TicketDetailView, TicketListView, TicketView, WageDetailView, WageListView, WageView

urlpatterns = patterns('',
                       # JOB
                       url(r'^jobindex/$', JobListView.as_view(), name='jobindex'),
                       url(r'^jobdetails/(?P<pk>\d+)/$', JobDetailView.as_view(), name='jobdetails'),
                       url(r'^addjob/$', JobView.as_view(), name='addjob'),

                       # TASK
                       url(r'^taskindex/$', TaskListView.as_view(), name='taskindex'),
                       url(r'^taskdetails/(?P<pk>\d+)/$', TaskDetailView.as_view(), name='taskdetails'),
                       url(r'^addtask/$', TaskView.as_view(), name='addtask'),

                       # TICKET
                       url(r'^ticketindex/$', TicketListView.as_view(), name='ticketindex'),
                       url(r'^ticketdetails/(?P<pk>\d+)/$', TicketDetailView.as_view(), name='ticketdetails'),
                       url(r'^addticket/$', TicketView.as_view(), name='addticket'),

                       # WAGE
                       url(r'^wageindex/$', WageListView.as_view(), name='wageindex'),
                       url(r'^wagedetails/(?P<pk>\d+)/$', WageDetailView.as_view(), name='wagedetails'),
                       url(r'^addwage/$', WageView.as_view(), name='addwage'),

)
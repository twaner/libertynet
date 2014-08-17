from django.conf.urls import patterns, url, include
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from Work.views import CreateEstimateView, ClientEstimateIndex, CreateSalesEstimateView, SalesEstimateIndex, \
    ClientEstimateDetails, SalesEstimateDetails, UpdatePartView, UpdateEstimateView, \
    update_part, add_part, UpdateJobView, JobIndexView, JobDetailsView, CreateJobView, \
    TicketIndexView, TicketDetailsView, CreateTicketView
#CreateEstimateStep2, , update_estimate


urlpatterns = patterns('',
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
                       # Static Views
                       url(r'^clientestimateindex/$', ClientEstimateIndex.as_view(), name='clientestimateindex'),
                       url(r'^estimatedetails/(?P<pk>[\d-]+)/$', ClientEstimateDetails.as_view(),
                           name='estimatedetails'),
                       # Create Views
                       url(r'^createestimate', CreateEstimateView.as_view(), name='createestimate'),
                       # url(r'^estimate_pt2/(?P<pk>[\d-]+)/$', CreateEstimateStep2.as_view(),
                       #     name='estimate_pt2'),
                       url(r'^updatepart/(?P<pk>[\d-]+)/(?P<part_pk>[\d-]+)/$', UpdatePartView.as_view(), name='updatepart'),
                       # url(r'^updatepart/(?P<pk>[\d-]+)/(?P<part_pk>[\d-]+)/$', update_part, name='updatepart'),
                       # url(r'^addpart/(?P<pk>[\d-]+)/$', addpart,
                       #     name='addpart'),
                       url(r'^add_part/(?P<pk>[\d-]+)/$', add_part,
                           name='add_part'),
                       # Update Views
                       # url(r'^updateestimate/(?P<pk>[\d-]+)/$', update_estimate, name='updateestimate'),
                       url(r'^updateestimate/(?P<pk>[\d-]+)/$', UpdateEstimateView.as_view(), name='updateestimate'),

                       ## Sales ##
                       # Static Views
                       url(r'^salesestimateindex/$', SalesEstimateIndex.as_view(), name='salesestimateindex'),
                       url(r'^salesestimatedetails/(?P<pk>\d+)/$', SalesEstimateDetails.as_view(), name='salesestimatedetails'),
                       # Create Views
                       url(r'^createsalesestimate', CreateSalesEstimateView.as_view(), name='createsalesestimate'),
                       # Update Views

                       ## Job ##
                       # Static Views
                       url(r'^jobindex/$', JobIndexView.as_view(), name='jobindex'),
                       url(r'^jobdetails/(?P<pk>[\d-]+)/$', JobDetailsView.as_view(), name='jobdetails'),
                       url(r'^addjob/$', CreateJobView.as_view(), name='addjob'),
                       url(r'^updatejob/(?P<pk>\d+)/$', UpdateJobView.as_view(), name='updatejob'),

                       ## Ticket ##
                       url(r'^ticketindex/$', TicketIndexView.as_view(), name='ticketindex'),
                       url(r'^ticketdetails/(?P<pk>[\d-]+)/$', TicketDetailsView.as_view(), name='ticketdetails'),
                       url(r'^addticket/$', CreateTicketView.as_view(), name='addticket'),

                       )

# urlpatterns += staticfiles_urlpatterns()
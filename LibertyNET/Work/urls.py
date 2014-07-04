from django.conf.urls import patterns, url, include
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from Work.views import CreateEstimateView, ClientEstimateIndex, CreateSalesEstimateView, SalesEstimateIndex, \
    ClientEstimateDetails, SalesEstimateDetails, CreateEstimateStep2, AddPartView, addpart, add_part, UpdateEstimateView


urlpatterns = patterns('',
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
                       # Static Views
                       url(r'^clientestimateindex/$', ClientEstimateIndex.as_view(), name='clientestimateindex'),
                       url(r'^estimatedetails/(?P<pk>[\d-]+)/$', ClientEstimateDetails.as_view(), name='estimatedetails'),
                       # Create Views
                       url(r'^createestimate', CreateEstimateView.as_view(), name='createestimate'),
                       url(r'^estimate_pt2/(?P<pk>[\d-]+)/$', CreateEstimateStep2.as_view(),
                           name='estimate_pt2'),
                       # url(r'^addpart/(?P<pk>[\d-]+)/$', AddPartView.as_view(),
                       #     name='addpart'),
                       # url(r'^addpart/(?P<pk>[\d-]+)/$', addpart,
                       #     name='addpart'),
                       url(r'^add_part/(?P<pk>[\d-]+)/$', add_part,
                           name='add_part'),
                       # Update Views
                       url(r'^updateestimate/(?P<pk>[\d-]+)/$', UpdateEstimateView.as_view(), name='updateestimate'),

                       ## Sales ##
                       # Static Views
                       url(r'^salesestimateindex/$', SalesEstimateIndex.as_view(), name='salesestimateindex'),
                       url(r'^salesestimatedetails/(?P<pk>\d+)/$', SalesEstimateDetails.as_view(), name='salesestimatedetails'),
                       # Create Views
                       url(r'^createsalesestimate', CreateSalesEstimateView.as_view(), name='createsalesestimate'),
                       # Update Views
                       )

# urlpatterns += staticfiles_urlpatterns()
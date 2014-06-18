from django.conf.urls import patterns, url
from Work.views import CreateEstimateView, ClientEstimateIndex, CreateSalesEstimateView, SalesEstimateIndex, \
    ClientEstimateDetails, SalesEstimateDetails


urlpatterns = patterns('',
                       # Static Views
                       url(r'^clientestimateindex/$', ClientEstimateIndex.as_view(), name='clientestimateindex'),
                       url(r'^estimatedetails/(?P<pk>\d+)/$', ClientEstimateDetails.as_view(), name='estimatedetails'),
                       # Create Views
                       url(r'^createestimate', CreateEstimateView.as_view(), name='createestimate'),

                       # Update Views

                       ## Sales ##
                       # Static Views
                       url(r'^salesestimateindex/$', SalesEstimateIndex.as_view(), name='salesestimateindex'),
                       url(r'^salesestimatedetails/(?P<pk>\d+)/$', SalesEstimateDetails.as_view(), name='salesestimatedetails'),
                       # Create Views
                       url(r'^createsalesestimate', CreateSalesEstimateView.as_view(), name='createsalesestimate'),
                       # Update Views
                       )


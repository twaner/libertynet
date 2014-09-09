from django.conf.urls import patterns, url, include
from Site.views import addclientsite, CreateSystemView, SystemDetailView, SystemIndexView, UpdateSystemView

urlpatterns = patterns('',
                       url(r'^systemindex/$', SystemIndexView.as_view(), name='systemindex'),
                       url(r'^systemdetails/(?P<pk>[\d-]+)/$', SystemDetailView.as_view(), name='systemdetails'),
                       url(r'^addsystem/$', CreateSystemView.as_view(), name='addsystem'),
                       url(r'^updatesystem/(?P<pk>[\d-]+)/$', UpdateSystemView.as_view(), name='updatesystem'),

                       # url(r'^clientestimateindex/$', ClientEstimateIndex.as_view(), name='clientestimateindex'),
                       # url(r'^estimatedetails/(?P<pk>[\d-]+)/$', ClientEstimateDetails.as_view(),

                      )

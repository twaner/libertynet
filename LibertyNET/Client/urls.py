from django.conf.urls import patterns, url
from views import ClientDetailView, ClientListView, SalesProspectView, SalesProspectListView, \
    ClientView, editclient, editsalesprospect, SalesProspectDetailView, salesprospectdetails

urlpatterns = patterns('',
    url(r'^index/$', ClientListView.as_view(), name='index'),
    url(r'^(?P<pk>[\d-]+)/$', ClientDetailView.as_view(), name='details'),
    url(r'^addclient/$', ClientView.as_view(), name='addclient'),
    url(r'editclient/(?P<client_id>\d+)/$', editclient, name='editclient'),
    url(r'^salesprospectindex/$', SalesProspectListView.as_view(), name='salesprospectindex'),
    #url(r'^salesprospectdetails/(?P<pk>[\d-]+)/$', SalesProspectDetailView.as_view(),
     #   name='salesprospectdetails'),
     url(r'^salesprospectdetails/(?P<sales_prospect_id>\d+)/$', salesprospectdetails,
         name='salesprospectdetails'),
    url(r'^addsalesprospect/$', SalesProspectView.as_view(), name='addsalesprospect'),
    url(r'^editsalesprospect/(?P<pk>\d+)/$', editsalesprospect, name='editsalesprospect'),
    #url(r'^editclient/(?P<pk>\d+)/$', EditClientView.as_view(), name='editclient'),
)


from django.conf.urls import patterns, url
from Client.views import ClientListView, ClientDetailView, ClientView, editclient, SalesProspectListView, \
    SalesProspectDetailView, SalesProspectView, editsalesprospect, convert_to_client, addclientcalllog, \
    CallLogDetailView, ClientCallLogIndex, addsalescalllog, SalesCallLogDetailView, SalesCallLogIndex, \
    ClientCallLogHome, SalesCallLogHome
from Common.views import addclientbilling, editclientbilling, addcalllist, updatecalllist, \
    CallListDetails
from Site.views import SiteDetailView

urlpatterns = patterns('',
                       url(r'^index/$', ClientListView.as_view(), name='index'),
                       url(r'^(?P<pk>[\d-]+)/$', ClientDetailView.as_view(), name='details'),
                       url(r'^addclient/$', ClientView.as_view(), name='addclient'),
                       url(r'editclient/(?P<pk>\d+)/$', editclient, name='editclient'),
                       url(r'addclientbilling/(?P<pk>[\d-]+)/$', addclientbilling,
                           name='addclientbilling'),
                       url(r'editclientbilling/(?P<pk>[\d-]+)/$', editclientbilling,
                           name='editclientbilling'),
                       url(r'addclientcalllist/(?P<pk>[\d-]+)/$', addcalllist,
                           name='addclientcalllist'),
                       url(r'sitedetails/(?P<pk>[\d-]+)/$', SiteDetailView.as_view(), name='sitedetails'),
                       url(r'calllistdetails/(?P<pk>[\d-]+)/$', CallListDetails.as_view(), name='calllistdetails'),
                       url(r'editclientcalllist/(?P<pk>[\d-]+)/$', updatecalllist, name='editclientcalllist'),
                       url(r'addclientcalllog/(?P<pk>[\d-]+)/$', addclientcalllog, name='addclientcalllog'),
                       url(r'clientcalllogdetails/(?P<pk>[\d-]+)/$', CallLogDetailView.as_view(),
                           name='clientcalllogdetails'),
                       url(r'clientcalllogindex/(?P<pk>[\d-]+)/$', ClientCallLogIndex.as_view(),
                           name='clientcalllogindex'),
                       url(r'^callloghome/$', ClientCallLogHome.as_view(), name='callloghome'),

                       # SalesProspect
                       url(r'^salesprospectindex/$', SalesProspectListView.as_view(), name='salesprospectindex'),
                       url(r'^salesprospectdetails/(?P<pk>\d+)/$', SalesProspectDetailView.as_view(),
                           name='salesprospectdetails'),
                       url(r'^addsalesprospect/$', SalesProspectView.as_view(), name='addsalesprospect'),
                       url(r'^editsalesprospect/(?P<pk>\d+)/$', editsalesprospect, name='editsalesprospect'),
                       url(r'salestoclient/(?P<pk>\d+)/$', convert_to_client, name='salestoclient'),
                       url(r'addsalescalllog/(?P<pk>\d+)/$', addsalescalllog, name='addsalescalllog'),
                       url(r'salescalllogdetails/(?P<pk>\d+)/$', SalesCallLogDetailView.as_view(),
                           name='salescalllogdetails'),
                       url(r'salescalllogindex/(?P<pk>\d+)/$', SalesCallLogIndex.as_view(),
                           name='salescalllogindex'),
                       url(r'^salescallloghome/$', SalesCallLogHome.as_view(), name='salescallloghome'),
)




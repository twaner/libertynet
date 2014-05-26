from django.conf.urls import patterns, url
from Client.views import ClientListView, ClientDetailView, ClientView, editclient, SalesProspectListView, \
    SalesProspectDetailView, SalesProspectView, editsalesprospect, convert_to_client, addclientcalllog, \
    CallLogDetailView, ClientCallLogIndex, addsalescalllog, SalesCallLogDetailView, SalesCallLogIndex, \
    ClientCallLogHome, SalesCallLogHome, ClientDetailViewWO, ClientDetailViewWrap, SalesProspectDetailViewWrap, \
    ClientCallLogView, editclientcall, EditClientCall

from Common.views import addclientbilling, editclientbilling, addcalllist, updatecalllist, \
    CallListDetails
from Site.views import SiteDetailView, addclientsite, editclientsite

urlpatterns = patterns('',
                       url(r'^index/$', ClientListView.as_view(), name='index'),
                       # TODO Remove --> test to show Work Order View
                       # Detail and Edit Views
                       url(r'clientdetails/(?P<pk>[\d-]+)/$', ClientDetailViewWO.as_view(), name='clientdetails'),
                       url(r'^(?P<pk>[\d-]+)/$', ClientDetailView.as_view(), name='details'),
                       url(r'clientdetails_wrap/(?P<pk>[\d-]+)/$', ClientDetailViewWrap.as_view(), name='clientdetails_wrap'),
                       url(r'^addclient/$', ClientView.as_view(), name='addclient'),
                       url(r'editclient/(?P<pk>\d+)/$', editclient, name='editclient'),
                       # Billing
                       url(r'addclientbilling/(?P<pk>[\d-]+)/$', addclientbilling,
                           name='addclientbilling'),
                       url(r'editclientbilling/(?P<pk>[\d-]+)/$', editclientbilling,
                           name='editclientbilling'),
                       # Call List
                       url(r'addclientcalllist/(?P<pk>[\d-]+)/$', addcalllist,
                           name='addclientcalllist'),
                       url(r'editclientcalllist/(?P<pk>[\d-]+)/$', updatecalllist, name='editclientcalllist'),
                       url(r'calllistdetails/(?P<pk>[\d-]+)/$', CallListDetails.as_view(), name='calllistdetails'),
                       # Site
                       url(r'sitedetails/(?P<pk>[\d-]+)/$', SiteDetailView.as_view(), name='sitedetails'),
                       # CallLog
                       url(r'addclientcalllog/(?P<pk>[\d-]+)/$', addclientcalllog, name='addclientcalllog'),
                       url(r'editclientcall/(?P<pk>[\d-]+)/$', editclientcall, name='editclientcall'),
                       url(r'clientcalllog_update_form/(?P<pk>[\d-]+)/$', EditClientCall.as_view(), name='clientcalllog_update_form'),
                       url(r'addcalllog/$', ClientCallLogView.as_view(), name='addcalllog'),
                       url(r'clientcalllogdetails/(?P<pk>[\d-]+)/$', CallLogDetailView.as_view(),
                           name='clientcalllogdetails'),
                       url(r'clientcalllogindex/(?P<pk>[\d-]+)/$', ClientCallLogIndex.as_view(),
                           name='clientcalllogindex'),
                       url(r'^callloghome/$', ClientCallLogHome.as_view(), name='callloghome'),
                       # Site
                       url(r'addclientsite/(?P<pk>[\d-]+)/$', addclientsite,
                           name='addclientsite'),
                       url(r'editclientsite/(?P<pk>[\d-]+)/$', editclientsite,
                           name='editclientsite'),

                       # SalesProspect
                       url(r'^salesprospectindex/$', SalesProspectListView.as_view(), name='salesprospectindex'),
                       url(r'^salesprospectdetails/(?P<pk>\d+)/$', SalesProspectDetailView.as_view(),
                           name='salesprospectdetails'),
                       url(r'^salesdetails_wrap/(?P<pk>\d+)/$', SalesProspectDetailViewWrap.as_view(),
                           name='salesdetails_wrap'),
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




__author__ = 'taiowawaner'
from django.conf.urls import patterns, url

from Vendor.views import SupplierDetailsView, SupplierIndexView, CreateSupplierView, EditSupplierView, \
    SupplierListIndexView, SupplierListDetailsView, CreateSupplierListView, EditSupplierListView, \
    ManufacturerIndexView, ManufacturerDetailsView, CreateManufacturerView, EditManufacturerView

urlpatterns = patterns('',
                       # # Supplier ##
                       url(r'^supplierindex/$', SupplierIndexView.as_view(), name='supplierindex'),
                       url(r'^supplierdetails/(?P<pk>[\d-]+)/$', SupplierDetailsView.as_view(), name='supplierdetails'),
                       url(r'^addsupplier/$', CreateSupplierView.as_view(), name='addsupplier'),
                       url(r'^editsupplier/$', EditSupplierView.as_view(), name='editsupplier'),
                       # # Supplier List##
                       url(r'^supplierlistindex/$', SupplierListIndexView.as_view(), name='supplierlistindex'),
                       url(r'^supplierlistdetails/(?P<pk>[\d-]+)/$', SupplierListDetailsView.as_view(), name='supplierlistdetails'),
                       url(r'^addsupplierlist/$', CreateSupplierListView.as_view(), name='addsupplierlist'),
                       url(r'^editsupplierlist/$', EditSupplierListView.as_view(), name='editsupplierlist'),
                       ## Manufacturer ##
                       url(r'^manufacturerindex/$', ManufacturerIndexView.as_view(), name='manufacturerindex'),
                       url(r'^manufacturerdetails/(?P<pk>[\d-]+)/$', ManufacturerDetailsView.as_view(), name='manufacturerdetails'),
                       url(r'^addmanufacturer/$', CreateManufacturerView.as_view(), name='addmanufacturer'),
                       url(r'^editmanufacturer/$', EditManufacturerView.as_view(), name='editmanufacturer'),
)

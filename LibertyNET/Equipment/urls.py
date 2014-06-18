from django.conf.urls import patterns, url
from Equipment.views import CreateInventoryPart, PartIndex, CreatePartCategory, UpdatePartInventory, \
    UpdatePartInventoryGeneric, PartDetailsView


urlpatterns = patterns('',
                       # Static Views
                       url(r'^index/$', PartIndex.as_view(), name='index'),
                       url(r'^partdetails/(?P<pk>\d+)/$', PartDetailsView.as_view(), name="partdetails"),
                       ## Change Part Info ##
                       url(r'^addpart/$', CreateInventoryPart.as_view(), name="addpart"),
                       url(r'^addpartcategory/$', CreatePartCategory.as_view(), name="addpartcategory"),
                       url(r'^updateinventory/$', UpdatePartInventoryGeneric.as_view(), name="updateinventory"),
                       url(r'^updatepartinventory/(?P<pk>\d+)/$', UpdatePartInventory.as_view(),
                           name="updatepartinventory"),

)

from django.shortcuts import render
from django.views.generic import CreateView
from models import Device, Camera, Panel, Part, ClientEstimate, \
    SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales
from Equipment.forms import DeviceForm, PanelForm, CameraForm, PartFormEstimate, ClientEstimateForm,\
SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm


# region Client Estimate


# endregion Client Estimate


# region Client Estimate


# endregion Client Estimate

# region Part

class CreateInventoryPart(CreateView):
    #model = Part
    form_class = PartFormEstimate
    template_name = 'equipment/addpart.html'



# endregion Part

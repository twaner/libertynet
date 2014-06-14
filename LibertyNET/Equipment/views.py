from django.shortcuts import render
from django.views.generic import CreateView, ListView
from models import Device, Camera, Panel, Part, ClientEstimate, \
    SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales, PartCategory
from Equipment.forms import DeviceForm, PanelForm, CameraForm, PartFormEstimate, PartCategoryForm, \
    ClientEstimateForm,\
SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm
from Vendor.models import Manufacturer


# region Part

class CreateInventoryPart(CreateView):
    """
    Creates a new Part for inventory. No location field.
    """
    #model = Part
    form_class = PartFormEstimate
    initial = {
        'is_active': True,
        'is_recalled': False,
    }
    template_name = 'equipment/addpart.html'
    success_url = 'equipment/index.html'

    def form_valid(self, form):
        return super(CreateInventoryPart, self).form_valid(form)


class PartIndex(ListView):
    model = Part
    context_object_name = 'parts'
    template_name = 'equipment/index.html'

    def get_context_data(self, **kwargs):
        context = super(PartIndex, self).get_context_data(**kwargs)
        context['vendors'] = Manufacturer.objects.all()
        context['part_category'] = PartCategory.objects.all()

        return context


class CreatePartCategory(CreateView):
    form_class = PartCategoryForm
    template_name = 'equipment/addpartcategory.html'
    success_url = 'equipment/index.html'

    def form_valid(self, form):
        return super(CreatePartCategory, self).form_valid(form)


# endregion Part

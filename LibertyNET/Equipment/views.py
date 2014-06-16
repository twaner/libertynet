from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from models import Device, Camera, Panel, Part, ClientEstimate, \
    SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales, PartCategory
from Equipment.forms import DeviceForm, PanelForm, CameraForm, PartFormEstimate, PartCategoryForm, \
    ClientEstimateForm, \
    SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm, PartFormInventory, PartFormInventoryRO
from Vendor.models import Manufacturer

#region Globals

equipment_index = 'equipment/index.html'

#endregion


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
    global equipment_index
    success_url = equipment_index

    def form_valid(self, form):
        return super(CreateInventoryPart, self).form_valid(form)


class PartIndex(ListView):
    model = Part
    context_object_name = 'parts'
    global equipment_index
    template_name = equipment_index

    def get_context_data(self, **kwargs):
        context = super(PartIndex, self).get_context_data(**kwargs)
        context['parts'] = Part.objects.all().order_by('-name', '-category')
        context['active_parts'] = Part.objects.filter(is_active=True)
        context['recalled_parts'] = Part.objects.filter(is_recalled=True)
        context['category_list'] = PartCategory.objects.values_list('category', flat=True)
        print('PartIndex %s' % context['category_list'])
        context['vendors'] = Manufacturer.objects.all()
        context['part_category'] = PartCategory.objects.all()

        return context


class PartDetailsView(DetailView):
    model = Part
    template_name = 'equipment/partdetails.html'
    context_object_name = 'part'

    def get_context_data(self, **kwargs):
        context = super(PartDetailsView, self).get_context_data(**kwargs)
        part = self.get_object()
        return context


class CreatePartCategory(CreateView):
    form_class = PartCategoryForm
    template_name = 'equipment/addpartcategory.html'
    global equipment_index
    success_url = reverse_lazy('Equipment:index')

    def form_valid(self, form):
        return super(CreatePartCategory, self).form_valid(form)

        # def get(self, request, *args, **kwargs):
        #     form = self.form_class(initial=self.initial)
        #     return render(request, self.template_name, {'form': form})
        #
        # def post(self, request, *args, **kwargs):
        #     self.object = None
        #     form_class = self.get_form_class()
        #     form = self.get_form(form_class)
        #     if form.is_valid():
        #         return HttpResponseRedirect('index')
        #     return render(request, self.template_name, {'form': form})


class UpdatePartInventoryGeneric(View):
    form_class = PartFormInventory
    template_name = 'equipment/updatepartinventory.html'
    global equipment_index
    success_url = equipment_index

    def form_valid(self, form):
        return super(UpdatePartInventory, self).form_valid(form)

    def get(self, request, **kwargs):
        form = PartFormInventory
        return render(request, self.template_name, {'form': form})


class UpdatePartInventory(UpdateView):
    form_class = PartFormInventoryRO
    model = Part
    template_name = 'equipment/updatepartinventory.html'

    def form_valid(self, form):
        print('UPDATE_INV %s ' % self.pk_url_kwarg)
        success_url = reverse_lazy('Equipment:partdetails',
                                   kwargs={
                                       'pk': self.pk_url_kwarg
                                   })
        return super(UpdatePartInventory, self).form_valid(form)

        # def get(self, request, **kwargs):
        #     form_class = self.get_form_class()
        #     #form = self.get_form(form_class=form_class)
        #     inital = self.get_initial()
        #     q = self.get_context_data()
        #     print('UpdatePartInventory -get_inital() %s' % inital, q)
        #     form = PartFormInventory
        #     return render(request, self.template_name, {'form': form})

# endregion Part

#region Spare Code


 # def get_object(self, queryset=None):
    #     obj = Part.objects.get(pk=self.kwargs['pk'])
    #     print('update inventory - get_object %s ' % obj.id)
    #     return obj

    #success_url = reverse_lazy('Equipment:partdetails')
    # success_url = reverse_lazy('Equipment:partdetails',
    #                                kwargs={
    #                                    'pk':
    #                                })

    # def get_context_data(self, **kwargs):
    #     part = super(UpdatePartInventory, self).get_context_data(**kwargs)
    #     part = self.get_object()
    #     return part

    # def get_object(self, queryset=None):
    #     obj = Part.objects.get(pk=2)
    #     return object
    #
    #

#endregion
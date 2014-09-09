from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
from django.core import serializers
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from django.views.generic.detail import SingleObjectMixin

from Vendor.models import Supplier, SupplierList, Manufacturer
from Vendor.forms import SupplierForm, ManufacturerForm, SupplierListForm
from Vendor.helpermethods import create_supplier_helper
from Common.forms import ContactForm
from Common.helpermethods import dict_generator, form_generator, validation_helper, create_contact_helper

# region Supplier


class SupplierIndexView(ListView):
    model = Supplier
    context_object_name = 'supplier'
    template_name = 'vendor/supplierindex.html'


class SupplierDetailsView(DetailView):
    model = Supplier
    context_object_name = 'supplier'
    template_name = 'vendor/supplierdetails.html'


class CreateSupplierView(CreateView):
    model = Supplier
    forms = form_generator(2)
    form_class = SupplierForm
    second_form = ContactForm
    template_name = 'vendor/addsupplier.html'

    def get_context_data(self, **kwargs):
        obj = self.get_object(queryset=None)
        context = super(CreateSupplierView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = super(CreateSupplierView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        self.forms[0] = self.form_class(request.POST)
        self.forms[1] = self.second_form(request.POST)

        if validation_helper(form_list=self.forms):
            contact = create_contact_helper(self.forms[1])
            supplier = create_supplier_helper(self.forms[0], contact)
            return HttpResponseRedirect(reverse('Vendor:supplierdetails',
                                                kwargs=dict(pk=supplier.supplier_id)))
        else:
            return render(request, self.template_name, dict_generator(self.forms))

    def get(self, request, *args, **kwargs):
        self.forms[0] = SupplierForm()
        self.forms[0] = ContactForm()
        form_dict = dict_generator(self.forms)

        return render(request, self.template_name, form_dict)


class EditSupplierView(UpdateView):
    pass


# endregion

# region SupplierList


class SupplierListIndexView(ListView):
    model = SupplierList
    context_object_name = 'supplier'
    template_name = 'work/clientestimateindex.html'


class SupplierListDetailsView(DetailView):
    model = SupplierList
    context_object_name = 'supplier'
    template_name = 'work/clientestimateindex.html'


class CreateSupplierListView(CreateView):
    pass


class EditSupplierListView(UpdateView):
    pass


# endregion

# region Manufacturer


# class SupplierListView(ListView):
#     model = Supplier
#     context_object_name = 'supplier'
#     template_name = 'work/clientestimateindex.html'
#
#
# class SupplierDetailsView(DetailView):
#     model = Supplier
#     context_object_name = 'supplier'
#     template_name = 'work/clientestimateindex.html'
#
#
# class CreateSupplierView(CreateView):
#     pass
#
#
# class EditSupplierView(UpdateView):
#     pass

# endregion
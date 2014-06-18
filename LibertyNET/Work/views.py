from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from Work.models import ClientEstimate, SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales
from Work.forms import ClientEstimateForm, SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm
from Equipment.models import Part, PartCategory


#region Index Views

class ClientEstimateIndex(ListView):
    model = ClientEstimate
    context_object_name = 'estimate'
    template_name = 'work/clientestimateindex.html'

    def get_context_data(self, **kwargs):
        context = super(ClientEstimateIndex, self).get_context_data(**kwargs)
        return context


class SalesEstimateIndex(ListView):
    model = SalesEstimate
    context_object_name = 'estimate'
    template_name = 'work/salesestimateindex.html'

    def get_context_data(self, **kwargs):
        context = super(SalesEstimateIndex, self).get_context_data(**kwargs)
        return context


#endregion


#region Detail Views


class ClientEstimateDetails(DetailView):
    model = ClientEstimate
    context_object_name = 'estimate'
    template_name = 'work/estimatedetails.html'

    def get_context_data(self, **kwargs):
        context = super(ClientEstimateIndex, self).get_context_data(**kwargs)
        return context


class SalesEstimateDetails(DetailView):
    model = SalesEstimate
    context_object_name = 'estimate'
    template_name = 'work/salesestimatedetails.html'

    def get_context_data(self, **kwargs):
        context = super(SalesEstimateIndex, self).get_context_data(**kwargs)
        return context

#endregion

#region Create Views


# class CreateEstimateStartView(CreateView):
#     form_class = EstimatePartsClientForm


class CreateEstimateView(CreateView):
    form_class = ClientEstimateForm
    template_name = 'work/createestimate.html'
    success_url = reverse_lazy('Work:estimatedetails')

    def form_valid(self, form):
        return super(CreateEstimateView, self).form_valid(form)


class CreateSalesEstimateView(CreateView):
    form_class = SalesEstimateForm
    template_name = 'work/createestimate.html'
    success_url = reverse_lazy('Work:salesestimatedetails')

    def form_valid(self, form):
        return super(CreateSalesEstimateView, self).form_valid(form)

#endregion

#region Update Views




#endregion

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from Work.models import ClientEstimate, SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales
from Work.forms import ClientEstimateForm, SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm, \
    JobForm
from Work.helpermethods import create_estimate_step_one
from Equipment.models import Part, PartCategory
from Common.helpermethods import validation_helper, form_generator, dict_generator


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
        context = super(ClientEstimateDetails, self).get_context_data(**kwargs)
        estimate = self.get_object()
        context['parts'] = estimate.estimate_parts.all()
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
    print('CreateEstimateView CALLED')

    def form_valid(self, form):

        estimate = form.save()
        success_url = reverse_lazy(estimate.get_absolute_url())
        return super(CreateEstimateView, self).form_valid(form)

    def form_invalid(self, form):
        validation_helper(form_list=form)
        return super(CreateEstimateView, self).form_invalid(form)


def addpart(request, pk):
    form_list = form_generator(1)
    template_name = 'work/addpart.html'
    model = Estimate_Parts_Client
    est_dict = {
        'estimate_id': 
    }

    estimate = ClientEstimate.objects.get(pk=pk)
    form_list[0] = EstimatePartsClientForm(request.POST)
    if request.method == 'POST':
        if validation_helper(form_list):
            form_list[0].save()
            return HttpResponseRedirect(reverse_lazy(estimate.get_absolute_url()))
        else:
            form_list[0] = EstimatePartsClientForm()
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = EstimatePartsClientForm()
        return render(request, template_name, dict_generator(form_list))



class AddPartView(UpdateView):
    form_class = EstimatePartsClientForm
    template_name = 'work/addpart.html'
    model = Estimate_Parts_Client

    def form_valid(self, form):
        success_url = reverse_lazy(estimate.get_absolute_url())
        return super(AddPartView, self).form_valid()

    def form_invalid(self, form):
        validation_helper(form_list=form)
        return super(AddPartView, self).form_invalid(form)


class CreateEstimateStep2(UpdateView):
    form_class = EstimatePartsClientForm
    model = ClientEstimate
    template_name = 'work/createestimate_pt2.html'
    success_url = reverse_lazy('Work:estimatedetails')
    template_name = 'work/createestimate_pt2.html'
    success_url = reverse_lazy('Work:estimatedetails')
    #context_object_name = 'estimate'
    print('CreateEstimateStep2 CALLED')
    #
    # def get(self, request, *args, **kwargs):
    #     def get_context_data(self, **kwargs):
    #         context = super(CreateEstimateStep2, self).get_context_data()
    #         return context
    #     context = get_context_data()
    #     print('CreateEstimateStep2 get CALLED %s' % context)
    #     return render(request, self.template_name, context)

    def form_valid(self, form):
        return super(CreateEstimateStep2, self).form_valid(form)

    def form_invalid(self, form):
        validation_helper(form_list=form)
        return super(CreateEstimateStep2, self).form_invalid(form)


class CreateSalesEstimateView(CreateView):
    form_class = SalesEstimateForm
    template_name = 'work/createestimate.html'
    success_url = reverse_lazy('Work:salesestimatedetails')

    def form_valid(self, form):
        return super(CreateSalesEstimateView, self).form_valid(form)

    def form_invalid(self, form):
        validation_helper(form_list=form)
        print('CreateEstimateStep2 -form_invalid %s ' % form)
        return super(CreateSalesEstimateView, self).form_invalid(form)


class CreateSalesEstimateStep2(UpdateView):
    form_class = EstimatePartsSalesForm
    template_name = 'work/createsalesestimate_pt2'
    success_url = reverse_lazy('Work:salesestimatedetails')

    def form_valid(self, form):
        return super(CreateSalesEstimateStep2, self).form_valid(form)

#endregion

#region Update Views




#endregion

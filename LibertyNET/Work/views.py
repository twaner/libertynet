from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from Work.models import ClientEstimate, SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales
from Work.forms import ClientEstimateForm, SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm, \
    JobForm
from Work.helpermethods import create_estimate_step_one,add_part_helper
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
    client = ClientEstimate.objects.get(pk=pk)
    est_dict = {
        'estimate_id': client
    }

    estimate = ClientEstimate.objects.get(pk=pk)
    form_list[0] = EstimatePartsClientForm(request.POST)
    if request.method == 'POST':
        if validation_helper(form_list):
            form_list[0].save()
            return HttpResponseRedirect(reverse_lazy(estimate.get_absolute_url()))
        else:
            form_list[0] = EstimatePartsClientForm(est_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = EstimatePartsClientForm(est_dict)
        return render(request, template_name, dict_generator(form_list))


class AddPartView(UpdateView):
    form_class = EstimatePartsClientForm
    template_name = 'work/addpart.html'
    model = ClientEstimate
    # def get_initial(self):
    #     return {
    #         'quantity': 0
    #     }
    initial = {
        'quantity': '0'
    }

    print('AddPartView called')

    def get_success_url(self):
        obj = self.get_object(queryset=None)
        return reverse_lazy(obj.get_absolute_url())

    def form_valid(self, form):
        success_url = reverse_lazy(self.get_absolute_url())
        return super(AddPartView, self).form_valid()

    # def form_invalid(self, form):
    #     validation_helper(form_list=form)
    #     return super(AddPartView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPartView, self).get_context_data(**kwargs)
        context['estimate'] = self.object
        print('addpartview context %s' % context)
        return context

    # def get_object(self, queryset=None):
    #     r = self.model
    #     print('get_object %s ' % r)
    #     return r
    #
    def get(self, request, **kwargs):
        form = EstimatePartsClientForm
        print('addpartget - kwargs %s' % self.pk_url_kwarg)
        return render(request, self.template_name, {'form': form})


def add_part(request, pk):
    form_list = form_generator(1)
    estimate = ClientEstimate.objects.get(pk=pk)
    form_class = EstimatePartsClientForm
    template_name = 'work/addpart.html'
    part_dict = {
        'quantity': '0'
    }
    if request.method == 'POST':
        form_list[0] = EstimatePartsClientForm(request.POST)
        if validation_helper(form_list):
            estimate = add_part_helper(form_list[0], estimate)
            return HttpResponseRedirect(
                reverse_lazy(estimate.get_absolute_url()))
    else:
        form_list[0] = EstimatePartsClientForm(part_dict)
        form_dict = form_generator(form_list)
        form_dict['est'] = estimate
        return render(request, template_name, form_dict)



class CreateEstimateStep2(UpdateView):
    form_class = EstimatePartsClientForm
    model = ClientEstimate
    template_name = 'work/createestimate_pt2.html'
    success_url = reverse_lazy('Work:estimatedetails')
    template_name = 'work/createestimate_pt2.html'
    success_url = reverse_lazy('Work:estimatedetails')
    #context_object_name = 'estimate'
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

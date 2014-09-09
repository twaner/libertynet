from django.shortcuts import render
from django.db.models import Count, Min, Sum, Avg
from django.core import serializers
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, View, DetailView
from django.views.generic.detail import SingleObjectMixin
from Work.models import ClientEstimate, SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales, Job, Ticket
from Work.forms import ClientEstimateForm, SalesEstimateForm, EstimatePartsClientForm, EstimatePartsSalesForm, \
    JobForm, UpdateClientEstimateForm, UpdateJobForm, TicketForm
from Work.helpermethods import add_part_helper, update_estimate_helper, create_estimate_helper, create_job_helper, \
    update_job_helper, create_ticket_helper
from Equipment.models import Part, PartCategory
from Site.models import Site
from Common.models import Address, Contact, Notes
from Common.forms import CallListContactForm, NotesForm
from Common.helpermethods import validation_helper, form_generator, dict_generator, create_notes_helper, \
    create_calllist_contact_helper
from Site.models import System


# region Index Views


class ClientEstimateIndex(ListView):
    """
    Index view for Client Estimates.
    """
    model = ClientEstimate
    context_object_name = 'estimate'
    template_name = 'work/clientestimateindex.html'

    def get_context_data(self, **kwargs):
        context = super(ClientEstimateIndex, self).get_context_data(**kwargs)
        client_estimates = ClientEstimate.objects.all()
        ser = serializers.serialize('json', client_estimates,
                                    fields=('job_name', 'listed_price', 'listed_profit', 'custom_sales_commission'))

        # tmp = list(client_estimates.values_list('job_name', 'listed_price', 'listed_profit'))
        context['estimate_list'] = json.dumps(ser)
        dollar_dict = client_estimates.aggregate(Sum('listed_price'), Sum('listed_profit'))
        context['price'] = dollar_dict['listed_price__sum']
        context['profit'] = dollar_dict['listed_profit__sum']
        print(context['estimate_list'])
        return context


class SalesEstimateIndex(ListView):
    """
    Index view for Sales Estimates.
    """
    model = SalesEstimate
    context_object_name = 'estimate'
    template_name = 'work/salesestimateindex.html'

    def get_context_data(self, **kwargs):
        context = super(SalesEstimateIndex, self).get_context_data(**kwargs)
        return context


# endregion


# region Detail Views


class ClientEstimateDetails(DetailView):
    """
    Details View for a Client Estimate
    """
    model = ClientEstimate
    context_object_name = 'estimate'
    template_name = 'work/estimatedetails.html'

    def get_context_data(self, **kwargs):
        context = super(ClientEstimateDetails, self).get_context_data(**kwargs)
        estimate = self.get_object()
        context['parts'] = estimate.estimate_parts.all()
        return context


class SalesEstimateDetails(DetailView):
    """
    Details View for a Sales Estimate
    """
    model = SalesEstimate
    context_object_name = 'estimate'
    template_name = 'work/salesestimatedetails.html'

    def get_context_data(self, **kwargs):
        context = super(SalesEstimateIndex, self).get_context_data(**kwargs)
        return context


# endregion

# region Create Views


class CreateEstimateView(CreateView):
    """
    Creates a Client Estimate object.
    """
    form_class = ClientEstimateForm
    template_name = 'work/createestimate.html'
    form_list = form_generator(1)

    # def form_valid(self, form):
    #     print('CreateEstimateView FORMCLEANED %s ' % form.cleaned_date['estimate_address'])
    #     estimate = form.save()
    #     print('CreateEstimateView ESTIMATE %s' % estimate.estimate_address)
    #     success_url = reverse_lazy(estimate.get_absolute_url())
    #     return super(CreateEstimateView, self).form_valid(form)
    #
    # def form_invalid(self, form):
    #     # print('CreateEstimateView %s ' % form)

    # validation_helper(form_list=form)
    # return super(CreateEstimateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        self.object = self.get_object(queryset=None)
        context = super(CreateEstimateView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        object = super(CreateEstimateView, self).get_object()
        return object

    def post(self, request, *args, **kwargs):
        self.form_list[0] = ClientEstimateForm(request.POST)
        print('Create estimate view Post estimate address {0}'.format(request.POST['estimate_address']))
        print('Create estimate view Post estimate client {0}'.format(request.POST['estimate_client']))
        print('Create Estimate Client {0} Address {1}'.format(self.form_list[0]['estimate_client'].value(),
                                                              self.form_list[0]['estimate_address'].value()))

        if validation_helper(self.form_list[0]):
            estimate = create_estimate_helper(self.form_list[0])
            return HttpResponseRedirect(reverse('Work:estimatedetails', kwargs={
                'pk': estimate.id
            }))
        else:
            return render(request, self.template_name, {'form': self.form_list[0]})

    def get(self, request, *args, **kwargs):
        form = self.form_class
        # context = {'estimate_address': None}
        # form = CourseBook(initial = {'course': course.pk})
        form(initial={'estimate_address': Address.pk})

        return render(request, self.template_name, {'form': form, })


def add_part(request, pk):
    """
    Adds a Part to an Estimate object.
    @param request: request.
    @param pk: primary key of Estimate.
    @return: http response.
    """
    form_list = form_generator(1)
    estimate = ClientEstimate.objects.get(pk=pk)
    form_class = EstimatePartsClientForm
    template_name = 'work/addpart.html'
    part_dict = {
        'quantity': '0', 'estimate_id': estimate
    }
    if request.method == 'POST':
        form_list[0] = EstimatePartsClientForm(request.POST)
        if validation_helper(form_list):
            estimate = add_part_helper(form_list[0], estimate)
            return HttpResponseRedirect(reverse('Work:estimatedetails',
                                                kwargs={'pk': estimate.id}))
        else:
            return render(request, template_name, dict_generator(form_list))

    else:
        print('ADD_PART CALLED!!')
        form_list[0] = EstimatePartsClientForm(part_dict)
        form_dict = {'form0': form_list[0], 'estimate': estimate}
        return render(request, template_name, form_dict)


class UpdatePartView(UpdateView):
    form_class = EstimatePartsClientForm
    template_name = 'work/addpart.html'
    model = ClientEstimate
    form_list = form_generator(1)

    def get_context_data(self, **kwargs):
        self.object = self.get_object(queryset=None)
        context = super(UpdatePartView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        object = super(UpdatePartView, self).get_object()
        return object

    def post(self, request, *args, **kwargs):
        estimate = self.get_object()
        self.form_list[0] = EstimatePartsClientForm(request.POST)
        if validation_helper(self.form_list):
            estimate = add_part_helper(self.form_list[0], estimate)
            return HttpResponseRedirect(reverse('Work:estimatedetails',
                                                kwargs={'pk': estimate.id}))

    def get(self, request, pk, part_pk, **kwargs):
        estimate = self.get_object()
        estimate_parts = estimate.estimate_parts.filter(part_id=part_pk)[0]
        est_parts_dict = {
            'part_id': estimate_parts.part_id, 'quantity': estimate_parts.quantity,
            'final_cost': estimate_parts.final_cost, 'cost': estimate_parts.cost,
            'sub_total': estimate_parts.sub_total, 'profit': estimate_parts.profit,
            'flat_total': estimate_parts.flat_total, 'total_labor': estimate_parts.total_labor,
        }
        form = EstimatePartsClientForm(est_parts_dict)
        context = self.get_context_data()
        context['estimate'] = estimate
        part = estimate_parts.part_id
        return render(request, self.template_name, {'form0': form, 'estimate': estimate, 'part': part})


def update_part(request, pk, part_pk):
    form_class = EstimatePartsClientForm
    template_name = 'work/addpart.html'
    form_list = form_generator(1)
    estimate = ClientEstimate.objects.get(pk=pk)
    estimate_parts = estimate.estimate_parts.filter(part_id=part_pk)[0]
    est_parts_dict = {
        'part_id': estimate_parts.part_id, 'quantity': estimate_parts.quantity,
        'final_cost': estimate_parts.final_cost, 'cost': estimate_parts.cost,
        'sub_total': estimate_parts.sub_total, 'profit': estimate_parts.profit,
        'flat_total': estimate_parts.flat_total, 'total_labor': estimate_parts.total_labor,
    }

    if request.method == 'POST':
        form_list[0] = EstimatePartsClientForm(request.POST)
        if validation_helper(form_list):
            estimate = add_part_helper(form_list[0], estimate)
            return HttpResponseRedirect('Work:estimatedetails',
                                        kwargs={'pk': estimate.id})
        else:
            return render(request, template_name, dict_generator(form_list))

    else:
        form_list[0] = EstimatePartsClientForm(est_parts_dict)
        part = estimate_parts.part_id
        form_dict = {'form0': form_list[0], 'estimate': estimate, 'part': part}
        return render(request, template_name, form_dict)


class CreateSalesEstimateView(CreateView):
    """
    Creates a Sales Estimate object.
    """
    form_class = SalesEstimateForm
    template_name = 'work/createestimate.html'
    success_url = reverse_lazy('Work:salesestimatedetails')

    def form_valid(self, form):
        return super(CreateSalesEstimateView, self).form_valid(form)

    def form_invalid(self, form):
        validation_helper(form_list=form)
        return super(CreateSalesEstimateView, self).form_invalid(form)


class CreateSalesEstimateStep2(UpdateView):
    form_class = EstimatePartsSalesForm
    template_name = 'work/createsalesestimate_pt2'
    success_url = reverse_lazy('Work:salesestimatedetails')

    def form_valid(self, form):
        return super(CreateSalesEstimateStep2, self).form_valid(form)


#endregion

#region Update Views


class UpdateEstimateView(UpdateView):
    """
    Updates an Estimate object by allowing custom pricing.
    """
    form_class = UpdateClientEstimateForm
    template_name = 'work/createestimate.html'
    model = ClientEstimate
    form_list = form_generator(1)

    def post(self, request, *args, **kwargs):
        self.form_list[0] = UpdateClientEstimateForm(request.POST)
        if validation_helper(self.form_list[0]):
            estimate = self.get_object(queryset=None)
            estimate = update_estimate_helper(self.form_list[0], estimate)
            return HttpResponseRedirect(reverse('Work:estimatedetails',
                                                kwargs={'pk': estimate.id}))
        else:
            self.form_list[0] = UpdateClientEstimateForm()
            return render(request, self.template_name, {'form': self.form_list[0]})

    def get(self, request, *args, **kwargs):
        obj = ClientEstimate.objects.get(pk=self.kwargs['pk'])
        est_dict = {
            'job_name': obj.job_name, 'margin': obj.margin, 'listed_price': obj.listed_price,
            'custom_sales_commission': obj.custom_sales_commission
        }
        self.form_list[0] = UpdateClientEstimateForm(est_dict)
        return render(request, self.template_name, {'form': self.form_list[0]})


#endregion

# region Job

class JobIndexView(ListView):
    model = Job
    context_object_name = 'job'
    template_name = 'work/jobindex.html'

    def get_context_data(self, **kwargs):
        context = super(JobIndexView, self).get_context_data(**kwargs)
        return context


class JobDetailsView(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'work/jobdetails.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailsView, self).get_context_data(**kwargs)
        context['address_detail'] = Address.objects.get(pk=context['job'].job_address.id)
        context['employees'] = list(context['job'].job_employee.all())
        return context


class CreateJobView(CreateView):
    model = Job
    template_name = 'work/addjob.html'
    form_list = form_generator(1)
    form_class = JobForm

    def get_context_data(self, **kwargs):
        obj = self.get_object(queryset=None)
        context = super(CreateJobView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = super(CreateJobView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        self.form_list[0] = JobForm(request.POST)

        if validation_helper(self.form_list[0]):
            job = create_job_helper(self.form_list[0])
            return HttpResponseRedirect(reverse('Work:jobdetails', kwargs={
                'pk': job.id
            }))

        else:
            return render(request, self.template_name, {
                'form': self.form_list[0]})

    def get(self, request, *args, **kwargs):
        self.form_list[0] = self.form_class()
        form = self.form_list[0]
        return render(request, self.template_name, {
            'form': form})


class UpdateJobView(UpdateView):
    """
    Updates a Job object.
    """
    form_class = UpdateJobForm
    template_name = 'work/updatejob.html'
    model = Job
    form_list = form_generator(1)

    def post(self, request, *args, **kwargs):
        self.form_list[0] = UpdateJobForm(request.POST)
        if validation_helper(self.form_list[0]):
            job = self.get_object(queryset=None)
            job = update_job_helper(job, self.form_list[0])
            return HttpResponseRedirect(reverse('Work:jobdetails', kwargs={
                'pk': job.id}))
        else:
            return render(request, self.template_name, {'form': self.form_list[0]})

    def get(self, request, *args, **kwargs):
        job = Job.objects.get(pk=self.kwargs['pk'])

        employees = [val for val in job.job_employee.all()]
        job_dict = {
            'name': job.name, 'job_employee': employees,
        }
        self.form_list[0] = UpdateJobForm(job_dict)
        return render(request, self.template_name, {'form': self.form_list[0]})


#endregion


#region Ticket


class TicketIndexView(ListView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'work/ticketindex.html'

    def get_context_data(self, **kwargs):
        context = super(TicketIndexView, self).get_context_data(**kwargs)
        return context


class TicketDetailsView(DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'work/ticketdetails.html'

    def get_context_data(self, **kwargs):
        context = super(TicketDetailsView, self).get_context_data(**kwargs)
        return context


class CreateTicketView(CreateView):
    model = Ticket
    template_name = 'work/addticket.html'
    form_list = form_generator(3)
    form_class = TicketForm
    second_form = NotesForm
    third_form = CallListContactForm

    def get_context_data(self, **kwargs):
        obj = self.get_object(queryset=None)
        context = super(CreateTicketView, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = super(CreateTicketView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        self.form_list[0] = self.form_class(request.POST)
        self.form_list[1] = self.second_form(request.POST)
        self.form_list[2] = self.third_form(request.POST)

        if validation_helper(form_list=self.form_list):
            notes = create_notes_helper(self.form_list[1])
            contact = create_calllist_contact_helper(self.form_list[2])
            ticket = create_ticket_helper(self.form_list[0], notes, contact)
            return HttpResponseRedirect(reverse('Work:ticketdetails', kwargs={
                                                            'pk': ticket.id
                                                        }))

        else:
            form_dict = dict_generator(self.form_list)
            return render(request, self.template_name, form_dict)

    def get(self, request, *args, **kwargs):
        self.form_list[0] = TicketForm()
        self.form_list[1] = NotesForm()
        self.form_list[2] = CallListContactForm()
        form_dict = dict_generator(self.form_list)

        return render(request, self.template_name, form_dict)


class CreateTicketOffJob(CreateTicketView):
    def get(self, request, *args, **kwargs):
        job = Job.objects.get(pk=self.kwargs['job'])
        system = System.objects.filter(system_client=job.job_client)
        ticket_dict = {
            'ticket_job': job, 'ticket_system': system,
        }
        self.form_list[0] = TicketForm(ticket_dict)
        self.form_list[1] = NotesForm()
        self.form_list[2] = CallListContactForm()
        form_dict = dict_generator(self.form_list)

        return render(request, self.template_name, form_dict)

# endregion
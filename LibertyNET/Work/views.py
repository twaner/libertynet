from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from models import Job, Task, Ticket, Wage
from Work.forms import JobForm, TaskForm, TicketForm, WageForm
from Work.helpermethods import create_job_helper, create_task_helper, create_ticket_helper, create_wage_helper
from Common.models import Address, Contact
from Employee.models import Employee
from Common.helpermethods import form_generator, dict_generator, validation_helper, create_address_helper
from Common.forms import AddressForm

#region JobViews


class JobListView(ListView):
    model = Job
    context_object_name = 'job_list'
    template_name = 'work/jobindex.html'


class JobDetailView(DetailView):
    model = Job
    id = 'pk'
    context_object_name = 'job_detail'
    template_name = 'work/jobdetails.html'

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        job = self.get_object()
        context['job_employee'] = job.job_employee.all()
        return context


class JobView(View):
    form_class = Job
    template_name = 'work/addjob.html'
    form_list = form_generator(2)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = JobForm(request.POST)
        form_list[1] = AddressForm(request.POST)

        if validation_helper(form_list):
            address = create_address_helper(form_list[1])
            job = create_job_helper(form_list[0], address)
            return HttpResponseRedirect(reverse('Work:jobdetails',
                                                kwargs={'pk': job.id}))
        else:
            return render(request, self.template_name, dict_generator(form_list))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = JobForm()
        form_list[1] = AddressForm()
        form_dict = dict_generator(form_list)
        return render(request, self.template_name, form_dict)


#endregion

#region TaskViews


class TaskListView(ListView):
    model = Task
    context_object_name = 'task_list'
    template_name = 'work/taskindex.html'


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task_detail'
    template_name = 'work/taskdetails.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        return context


class TaskView(View):
    form_class = Task
    template_name = 'work/addtask.html'
    form_list = form_generator(1)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = TaskForm(request.POST)

        if validation_helper(form_list):
            task = create_task_helper(request)

    def get(self, request, form_list=form_list, *args, **kwargs):
        pass

#endregion

#region TicketViews


class TicketListView(ListView):
    model = Ticket
    context_object_name = 'ticket_list'
    template_name = 'work/ticketindex.html'


class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket_detail'
    template_name = 'work/ticketdetails.html'

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        return context


class TicketView(View):
    form_class = Ticket
    template_name = 'work/addticket.html'
    form_list = form_generator(3)

    def post(self, request, form_list=form_list, *args, **kwargs):
        pass

    def get(self, request, form_list=form_list, *args, **kwargs):
        pass

#endregion

#region WageViews


class WageListView(ListView):
    model = Wage
    context_object_name = 'wage_list'
    template_name = 'work/wageindex.html'


class WageDetailView(DetailView):
    model = Wage
    context_object_name = 'wage_detail'
    template_name = 'work/wagedetails.html'

    def get_context_data(self, **kwargs):
        context = super(WageDetailView, self).get_context_data(**kwargs)
        return context


class WageView(View):
    form_class = Wage
    template_name = 'work/addwage.html'
    form_list = form_generator(1)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = WageForm(request.POST)

        if validation_helper(form_list):
            wage = create_wage_helper(form_list[0])
            return HttpResponseRedirect(reverse('Work:addwage',
                                                kwargs={'pk': wage.id}))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = WageForm()
        return request(request, self.template_name, dict_generator(form_list))



#endregion



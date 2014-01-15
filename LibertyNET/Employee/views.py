from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from models import Employee, Title
from forms import AddEmployeeForm, EmployeeForm
from helpermethods import create_employee_helper, create_employee_worker
from Common.models import Address, Contact
from Common.helpermethods import create_address_helper, create_employee_contact_helper, form_generator, \
    validation_helper, dict_generator
from Common.forms import AddressForm, EmployeeContactForm


#region ListViews


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'all_employees_list'
    template_name = 'employee/index.html'


class EmployeeDetailList(ListView):
    template_name = 'employee/detail.html'

    def get_queryset(self):
        self.employee = get_object_or_404(Employee, name=self.args[0])
        return Employee.objects.filter(employee=self.employee)

#endregion

#region DetailView


class EmployeeDetailView(DetailView):
    pass
    model = Employee

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
    

#endview


#region Employee Views


def addemployee(request):
    form_list = form_generator(3)
    if request.method == 'POST':
        form_list[0] = AddEmployeeForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = EmployeeContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(request)
            contact = create_employee_contact_helper(request)
            employee = create_employee_worker(request, address, contact)
            return HttpResponseRedirect('/employee/index/')
    else:
        form_list[0] = AddEmployeeForm()
        form_list[1] = AddressForm()
        form_list[2] = EmployeeContactForm()
    form_dict = dict_generator(form_list)

    return render(request, 'employee/addemployee.html', form_dict)


#endregion
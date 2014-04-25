from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse
from models import Employee, Title
from forms import AddEmployeeForm, EmployeeForm
from helpermethods import create_employee_helper, create_employee_worker, update_employee
from Common.helpermethods import create_address_helper, create_employee_contact_helper, form_generator, \
    validation_helper, dict_generator, update_address_helper, update_contact_employee_helper
from Common.forms import AddressForm, EmployeeContactForm
from Common.models import Address, Contact

#region ListViews


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'all_employees_list'
    template_name = 'employee/index.html'


class EmployeeDetailView(DetailView):
    model = Employee
    employee_id = 'pk'

    context_object_name = 'employee_detail'
    template_name = 'employee/details.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        employee = self.get_object()
        context['address_detail'] = Address.objects.get(pk=employee.emp_address_id)
        context['contact_detail'] = Contact.objects.get(pk=employee.emp_contact_id)
        context['title_detail'] = employee.emp_title.all()
        return context

#endregion

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
            return HttpResponseRedirect(reverse('Employee:index'))
    else:
        form_list[0] = AddEmployeeForm()
        form_list[1] = AddressForm()
        form_list[2] = EmployeeContactForm()
    form_dict = dict_generator(form_list)

    return render(request, 'employee/addemployee.html', form_dict)


def editemployee(request, pk):
    form_list = form_generator(3)
    employee = Employee.objects.get(pk=pk)
    address = Address.objects.get(pk=employee.emp_address_id)
    contact = Contact.objects.get(pk=employee.emp_contact_id)
    title_details = employee.emp_title.all()
    # create dictionaries to bind to forms
    employee_dict = {
        'first_name': employee.first_name, 'middle_initial': employee.middle_initial,
        'last_name': employee.last_name, 'emp_number': employee.emp_number,
        'emp_title': title_details, 'hire_date': employee.hire_date,
        'pay_type': employee.pay_type, 'pay_rate': employee.pay_rate,
        'is_terminated': employee.is_terminated, 'termination_date': employee.termination_date,
        'termination_reason': employee.termination_reason,
    }
    address_dict = {
        'street': address.street, 'unit': address.unit, 'city': address.city,
        'state': address.state, 'zip_code': address.zip_code
    }
    contact_dict = {
        'phone': contact.phone, 'cell': contact.cell, 'email': contact.email,
        'work_email': contact.work_email, 'office_phone': contact.office_phone,
        'office_phone_extension': contact.office_phone_extension
    }
    if request.method == 'POST':
        form_list[0] = EmployeeForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = EmployeeContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address_updated = update_address_helper(request, address)
            contact_updated = update_contact_employee_helper(request, contact)
            updated_employee = update_employee(request, employee, address_updated, contact_updated)
            return HttpResponseRedirect(reverse('Employee:index'))
    else:
        # Display bound forms
        form_list[0] = EmployeeForm(employee_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = EmployeeContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    return render(request, 'employee/editemployee.html', form_dict)


        #endregion
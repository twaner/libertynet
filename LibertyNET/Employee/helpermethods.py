from models import Employee
from Common.models import Address
from Common.helpermethods import str_to_cap

#region Employee Helper Methods


def create_employee_helper(form, *args):
    """
    Creates an employee object from a form.
    @param request: request.
    @param args: Address and Contact objects.
    @rtype : Employee
    @return: Employee.
    """
    first_name = form.cleaned_data.get('first_name')
    middle_initial = form.cleaned_data.get('middle_initial')
    last_name = form.cleaned_data.get('last_name')
    emp_number = form.cleaned_data.get('emp_number')
    hire_date = form.cleaned_data.get('hire_date')
    pay_type = form.cleaned_data.get('pay_type')
    pay_rate = form.cleaned_data.get('pay_rate')
    emp_title = form.cleaned_data.get('emp_title')
    #handle how *args are ordered
    if type(args[0]) == Address:
        emp_address = args[0]
        emp_contact = args[1]
    elif type(args[1]) == Address:
        emp_address = args[1]
        emp_contact = args[0]
    employee = Employee.objects.create_employee(first_name=first_name, middle_initial=middle_initial,
                                                last_name=last_name, emp_number=emp_number, emp_title=emp_title,
                                                emp_address=emp_address, emp_contact=emp_contact,
                                                hire_date=hire_date, pay_type=pay_type, pay_rate=pay_rate)
    employee.save(commit=False)
    [employee.emp_title.add(et) for et in form.cleaned_data.getlist('emp_title')]
    employee.save()
    return employee


def update_employee(form, employee, address, contact):
    """
    Updates an Employee.
    @param request: request.
    @param employee: Employee.
    @param address: Employee's address.
    @param contact: Employee's contact.
    """
    employee.first_name = str_to_cap(form.cleaned_data.get('first_name'))
    employee.middle_initial = str(form.cleaned_data.get('middle_initial')).upper()
    employee.last_name = str_to_cap(form.cleaned_data.get('last_name'))
    employee.emp_number = form.cleaned_data.get('emp_number')
    employee.emp_address = address
    employee.emp_contact = contact
    employee.hire_date = form.cleaned_data.get('hire_date')
    employee.pay_type = form.cleaned_data.get('pay_type')
    employee.pay_rate = form.cleaned_data.get('pay_rate')
    emp_title = form.cleaned_data.get('emp_title')
    employee.is_terminated = form.cleaned_data.get('is_terminated')
    if employee.is_terminated is None:
        employee.is_terminated = False
    employee.termination_date = form.cleaned_data.get('termination_date')
    if employee.termination_date == '' or employee.termination_date is None:
        employee.termination_date = None
    employee.termination_reason = form.cleaned_data.get('termination_reason')
    # Handle titles
    et_list = []
    [et_list.append(unicode(t.title_id)) for t in employee.emp_title.all()]
    [employee.emp_title.add(t) for t in emp_title if t not in et_list]
    [employee.emp_title.remove(t) for t in et_list if t not in emp_title]
    # [t.remove(i) for i in t if i not in r] set(t+r)
    employee.save(update_fields=['first_name', 'middle_initial', 'last_name', 'emp_number', 'emp_address',
                                 'emp_contact', 'hire_date', 'pay_type', 'pay_type', 'is_terminated',
                                 'termination_date', 'termination_reason'])


def create_employee_worker(form, address, contact):
    """
    Creates a new employee object.
    @param request: request.
    @param args: address and contact.
    @rtype: Employee
    @return: Employee object.
    """
    first_name = form.cleaned_data.get('first_name')
    middle_initial = form.cleaned_data.get('middle_initial')
    last_name = form.cleaned_data.get('last_name')
    emp_number = form.cleaned_data.get('emp_number')
    hire_date = form.cleaned_data.get('hire_date')
    pay_type = form.cleaned_data.get('pay_type')
    pay_rate = form.cleaned_data.get('pay_rate')
    emp_titles = form.cleaned_data.get('emp_title')
    employee = Employee.objects.create_employee_short(first_name, middle_initial, last_name, emp_number, emp_titles,
                                                      address, contact, hire_date, pay_type, pay_rate)
    # [employee.emp_title.add(et) for et in form.cleaned_data.getlist('emp_title')]
    # employee.save()
    return employee

#endregion

#region TitleHelperMethods


def titles_to_pk_list(employee):
    """
    Takes an employee object's list and converts titles to flat list for a ModelForm
    @param employee: Employee object.
    @rtype: list
    @return: List of titles.
    """
    the_list = list(Employee.objects.values_list('emp_title', flat=True))
    return the_list

    #endregion
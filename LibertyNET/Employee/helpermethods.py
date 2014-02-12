from models import Employee
from Common.models import Address, Contact

#region Employee Helper Methods


def create_employee_helper(request, *args):
    """
    Creates an employee object from a form.
    @param request: request.
    @param args: Address and Contact objects.
    @rtype : Employee
    @return: Employee.
    """
    first_name = request.POST.get('first_name')
    middle_initial = request.POST.get('middle_initial')
    last_name = request.POST.get('last_name')
    emp_number = request.POST.get('emp_number')
    #emp_address = request.POST.get('emp_address')
    #emp_contact = request.POST.get('emp_contact')
    hire_date = request.POST.get('hire_date')
    pay_type = request.POST.get('pay_type')
    pay_rate = request.POST.get('pay_rate')
    emp_title = request.POST.getlist('emp_title')
    #handle how *args are ordered
    if type(args[0]) == Address:
        emp_address = args[0]
        emp_contact = args[1]
    elif type(args[1]) == Address:
        emp_address = args[1]
        emp_contact = args[0]
    employee = Employee.objects.create(first_name=first_name, middle_initial=middle_initial,
                                       last_name=last_name, emp_number=emp_number, emp_title=emp_title,
                                       emp_address=emp_address, emp_contact=emp_contact,
                                       hire_date=hire_date, pay_type=pay_type, pay_rate=pay_rate)
    employee.save(commit=False)
    [employee.emp_title.add(et) for et in request.POST.getlist('emp_title')]
    employee.save()
    return employee


def update_employee(request, employee, address, contact):
    employee.first_name = request.POST.get('first_name')
    employee.middle_initial = request.POST.get('middle_initial')
    employee.last_name = request.POST.get('last_name')
    employee.emp_number = request.POST.get('emp_number')
    employee.emp_address = address
    employee.emp_contact = contact
    employee.hire_date = request.POST.get('hire_date')
    employee.pay_type = request.POST.get('pay_type')
    employee.pay_rate = request.POST.get('pay_rate')
    emp_title = request.POST.getlist('emp_title')
    employee.is_terminated = request.POST.get('is_terminated')
    if employee.is_terminated is None:
        employee.is_terminated = False
    employee.termination_date = request.POST.get('termination_date')
    if employee.termination_date == '' or employee.termination_date is None:
        employee.termination_date = None
    employee.termination_reason = request.POST.get('termination_reason')

    # Handle titles
    et_list = []
    [et_list.append(unicode(t.title_id)) for t in employee.emp_title.all()]
    [employee.emp_title.add(t) for t in emp_title if t not in et_list]
    [employee.emp_title.remove(t) for t in et_list if t not in emp_title]
    # [t.remove(i) for i in t if i not in r] set(t+r)
    employee.save(update_fields=['first_name', 'middle_initial', 'last_name', 'emp_number', 'emp_address',
                                 'emp_contact', 'hire_date', 'pay_type', 'pay_type', 'is_terminated',
                                 'termination_date', 'termination_reason'])


def create_employee_worker(request, *args):
    """
    Creates a new employee object.
    @param request: request.
    @param args: address and contact.
    @rtype: Employee
    @return: Employee object.
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    emp_number = request.POST.get('emp_number')
    #emp_address = request.POST.get('emp_address')
    #emp_contact = request.POST.get('emp_contact')
    hire_date = request.POST.get('hire_date')
    pay_type = request.POST.get('pay_type')
    pay_rate = request.POST.get('pay_rate')
    #emp_title = request.POST.getlist('emp_title')
    if type(args[0]) == Address:
        emp_address = args[0]
        emp_contact = args[1]
    elif type(args[1]) == Address:
        emp_address = args[1]
        emp_contact = args[0]
    employee = Employee(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                        emp_number=emp_number, emp_address=emp_address, emp_contact=emp_contact,
                        hire_date=hire_date, pay_type=pay_type, pay_rate=pay_rate)
    employee.save()
    [employee.emp_title.add(et) for et in request.POST.getlist('emp_title')]
    employee.save()
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
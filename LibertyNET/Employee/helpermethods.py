from models import Employee
from Common.models import Address, Contact

#region Employee Helper Methods


def create_employee_helper(request, *args):
    """
    Creates an employee object from a form.
    @param request: request.
    @param args: Address and Contact objects.
    @return: Employee.
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    emp_number = request.POST.get('emp_number')
    #emp_address = request.POST.get('emp_address')
    #emp_contact = request.POST.get('emp_contact')
    hire_date = request.POST.get('hire_date')
    pay_type = request.POST.get('pay_type')
    pay_rate = request.POST.get('pay_rate')
    emp_title = request.POST.getlist('emp_title')
    #handle how *args are ordered
    if isinstance(type(args[0], Address)):
        emp_address = args[0]
        emp_contact = args[1]
    elif type(args[1]) == Address:
        emp_address = args[1]
        emp_contact = args[0]
    print("EMP_TITLE==>", emp_title)
    employee = Employee.objects.create(first_name=first_name, last_name=last_name, emp_number=emp_number,
                                       emp_title=emp_title, emp_address=emp_address, emp_contact=emp_contact,
                                       hire_date=hire_date, pay_type=pay_type, pay_rate=pay_rate)
    employee.save(commit=False)
    print("EMP_TITLE==>", emp_title)
    [employee.emp_title.add(et) for et in request.POST.getlist('emp_title')]
    employee.save()
    return employee


def create_employee_worker(request, *args):
    """
    Creates a new employee object.
    @param request: request.
    @param args: address and contact.
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
    emp_title = request.POST.getlist('emp_title')
    if type(args[0]) == Address:
        emp_address = args[0]
        emp_contact = args[1]
    elif type(args[1]) == Address:
        emp_address = args[1]
        emp_contact = args[0]
    employee = Employee(first_name=first_name, last_name=last_name, emp_number=emp_number,
                        emp_address=emp_address, emp_contact=emp_contact,
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
    @return: List of titles.
    """
    the_list = list(Employee.objects.values_list('emp_title', flat=True))
    return the_list

#endregion
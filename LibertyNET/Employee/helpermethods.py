from models import Employee
from Common.models import Address, Contact

#region Employee Helper Methods


def create_employee(request, *args):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    employee_number = request.POST.get('employee_number')
    hire_date = request.POST.get('hire_date')
    pay_type = request.POST.get('pay_type')
    pay_rate = request.POST.get('pay_rate')
    if type(args[0]) == Address:
        emp_address = args[0]
        emp_contact = args[1]
    elif type(args[1]) == Address:
        emp_address = args[1]
        emp_contact = args[0]
        employee = Employee.objects.create_employee(first_name, last_name, emp_number, emp_address,
                                                    emp_contact)
    [employee.emp_title.add(et) for et in request.POST.getlist('emp_title')]
    employee.save()
    return employee

#endregion
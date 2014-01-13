from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView
from models import Employee, Title
from Common.models import Address, Contact

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

#region Employee Views



#endregion
from django import forms
from models import Employee, Title
from bootstrap_toolkit.widgets import BootstrapDateInput


#region EmployeeForms


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['emp_address', 'emp_contact']
        widgets = {
            'hire_date': BootstrapDateInput,
            'termination_date': BootstrapDateInput,
            'termination_reason': forms.Textarea(attrs={'cols': 160, 'rows': 10})
        }

class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['emp_address', 'emp_contact', 'termination_reason', 'termination_date',
                   'is_terminated']

#endregion

#region TitleForm


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'

#endregion
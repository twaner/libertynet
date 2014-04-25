from django import forms
from models import Employee, Title
from django.utils.translation import gettext as _
from bootstrap_toolkit.widgets import BootstrapDateInput

#region Variables
employee_labels = {
    'emp_number': _('Employee Number'),
}

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
        labels = {
            'is_terminated': _('Terminate Employee'),
        }


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['emp_address', 'emp_contact', 'termination_reason', 'termination_date',
                   'is_terminated']
        labels = {
            'emp_number': _('Employee Number'),
        }
        widgets = {
            'hire_date': BootstrapDateInput,
        }

#endregion

#region TitleForm


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'

        #endregion
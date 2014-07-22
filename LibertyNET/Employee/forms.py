from django import forms
from models import Employee, Title
from django.utils.translation import gettext as _
from Common.helpermethods import date_picker_helper

#region Variables
employee_labels = {
    'emp_number': _('Employee Number'),
}

date_picker_css = date_picker_helper()

#region EmployeeForms


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['emp_address', 'emp_contact']
        widgets = {
            'hire_date':  forms.DateInput(attrs=date_picker_css),
            'termination_date':  forms.DateInput(attrs=date_picker_css),
            'termination_reason': forms.Textarea(attrs={'cols': 160, 'rows': 10}),
            'is_terminated': forms.CheckboxInput(attrs={'class': "iButton-icons"}),
            'pay_type': forms.Select(attrs={'class': 'form-control'}),
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
            'hire_date':  forms.DateInput(attrs=date_picker_css),
            'pay_type': forms.Select(attrs={'class': 'form-control'}),
        }

#endregion

#region TitleForm


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'

        #endregion
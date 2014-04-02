from django import forms
from django.utils.translation import gettext as _
from bootstrap_toolkit.widgets import BootstrapDateInput
from models import Job, Task, Ticket, Wage

#region ModelForms


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['job_address']
        labels = {
            'name': _('Job Name')
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'task_created_date': BootstrapDateInput,
            'task_completed_date': BootstrapDateInput,
            'task_note': forms.Textarea(attrs={
                'cols': 80, 'rows': 7
            }),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'scheduled_date': BootstrapDateInput,
            'scheduled_time': forms.TimeInput,
            'description_work': forms.Textarea(attrs={
                'cols': 80, 'rows': 7}),
            'technician_note': forms.Textarea(attrs={
                'cols': 80, 'rows': 7}),
            'start_time': forms.TimeInput,
            'start_date': BootstrapDateInput,
            'end_time': forms.TimeInput,
            'end_date': BootstrapDateInput,
            #'is_ticket_completed': forms.CheckboxInput
        }


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        exclude = ['gross_wage', 'total_hours']
        labels = {
            'wages_employee': _('Employee Name'),
            'wage_date': _('Date'),

        }
        widgets = {
            'wages_date': BootstrapDateInput,
            'wages_start_time': forms.TimeInput,
            'wages_end_time': forms.TimeInput,
            'wages_lunch_start': forms.TimeInput,
            'wages_lunch_end': forms.TimeInput,
        }


#endregiond

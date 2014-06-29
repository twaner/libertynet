from django import forms
from django.utils.translation import gettext as _
from bootstrap_toolkit.widgets import BootstrapDateInput
from Common.helpermethods import readonly_worker
from models import Job, Task, Ticket, Wage, ClientEstimate, Estimate_Parts_Client, \
    Estimate_Parts_Sales, SalesEstimate
from Equipment.models import Part

# region ModelForms


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'


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
            'is_ticket_completed': forms.CheckboxInput
        }


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        exclude = ['gross_wage']
        widgets = {
            'wages_date': BootstrapDateInput,
            'wages_start_time': forms.TimeInput,
            'wages_end_time': forms.TimeInput,
            'wages_lunch_start': forms.TimeInput,
            'wages_lunch_end': forms.TimeInput
        }
        labels = {
            'wages_employee': _('Employee Name'),
            'wage_date': _('Date'),
        }


# endregion

#region Estimates


class ClientEstimateForm(forms.ModelForm):
    class Meta:
        model = ClientEstimate
        fields = ['estimate_client', 'job_name', 'date', 'preparer',
                  'is_capital_improvement', 'margin', 'estimate_address']
        #           'margin_guidelines', 'estimate_address']
        # fields = ['job_name', 'date', 'preparer', 'is_capital_improvement', 'margin',
        #           'margin_guidelines', 'estimate_address']
        widgets = {
            'is_capital_improvement': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'estimate_address': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preparer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estimate_client': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
        }


class SalesEstimateForm(forms.ModelForm):
    class Meta:
        model = SalesEstimate
        fields = ['job_name', 'date', 'preparer', 'is_capital_improvement', 'margin',
                  'margin_guidelines', 'estimate_address']
        widgets = {
            'is_capital_improvement': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'estimate_address': forms.Select(attrs={
                'class': 'form-control'
            }),
            'preparer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estimate_client': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
        }


class EstimatePartsClientFormBase(forms.ModelForm):
    class Meta:
        model = Estimate_Parts_Client
        fields = ['part_id', 'quantity', 'cost', 'final_cost', 'sub_total',
                  'profit', 'flat_total', 'total_labor']
        widgets = {
            'part_id': forms.Select(attrs={
                'onchange': "Dajaxice.Work.get_part(Dajax.process,{"
                            "'pk': this.value"
                            "});",
                'class': 'form-control',
            }),
            # 'estimate_id': forms.Select(attrs={
            #     'class': 'form-control'
            # }),
            'quantity': forms.TextInput(attrs={
                'type': 'number',
                'min': '0',
            }),
        }
        # part_id = forms.ModelChoiceField(widget=forms.Select(attrs={
        #                                                      'onchange': "Dajaxice.Work.get_part(Dajax.process,{"
        #                                                                  "'pk':this.value"
        #                                                                  "});",
        #                                                      'class': 'form-control',
        # }),
        #                                  queryset=Part.objects.all(), required=True,
        #                                  # empty_label=Select Part, label=Part,
        #         #                          help_text=lcountry_help, error_messages={
        #         # 'required': lcountry_required}
        #     )


class EstimatePartsClientForm(EstimatePartsClientFormBase):
    def __init__(self, *args, **kwargs):
        super(EstimatePartsClientForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            field_list = ['quantity', 'cost', 'final_cost', 'sub_total',
                          'profit', 'flat_total', 'total_labor']
            readonly_worker(self, field_list)

    def clean_part(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.part
        else:
            return self.cleaned_data['estimate_parts_client']


class EstimatePartsSalesForm(forms.ModelForm):
    class Meta:
        model = Estimate_Parts_Sales
        fields = '__all__'

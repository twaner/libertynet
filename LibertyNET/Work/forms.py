from django import forms
from django.utils.translation import gettext as _
from bootstrap_toolkit.widgets import BootstrapDateInput
from Common.helpermethods import readonly_worker
from models import Job, Task, Ticket, Wage, ClientEstimate, Estimate_Parts_Client, \
    Estimate_Parts_Sales, SalesEstimate
from Common.models import Address
from Site.models import Site
from Equipment.models import Part

# region ModelForms


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

# region Estimates

class ClientEstimateFormOne(forms.ModelForm):
    class Meta:
        model = ClientEstimate
        fields = ['estimate_client']

        widgets = {
            'estimate_client': forms.Select(attrs={
                'class': 'form-control',
                'onchange': "Dajaxice.Work.get_sites(Dajax.process,{"
                            "'pk': this.value"
                            "});",
            }),
        }


class ClientEstimateForm(forms.ModelForm):
    estimate_address = forms.ModelChoiceField(queryset=Address.objects.all(),
                                              widget=forms.HiddenInput())

    class Meta:
        model = ClientEstimate
        fields = ['estimate_client', 'estimate_address', 'job_name', 'date',
                  'preparer', 'is_capital_improvement', 'margin', 'margin_guidelines']
        #           'margin_guidelines', 'estimate_address']
        widgets = {
            'is_capital_improvement': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            # 'estimate_address': forms.HiddenInput(),
            'preparer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'estimate_client': forms.Select(attrs={
                'class': 'form-control',
                'onchange': "Dajaxice.Work.get_sites(Dajax.process,{"
                            "'pk': this.value"
                            "});",
            }),
            'date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'margin_guidelines': forms.Textarea(attrs={'cols': 160, 'rows': 3,
                                                       'maxlength': ClientEstimate._meta.get_field(
                                                           'margin_guidelines').max_length,
                                                       'onkeyup': "charRemaining('id_margin_guidelines', "
                                                                  "'remaining_span')",
            }),
        }


class UpdateClientEstimateForm(forms.ModelForm):
    class Meta:
        model = ClientEstimate
        fields = ['job_name', 'margin', 'listed_price',
                  'custom_sales_commission']


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
        labels = {
            'part_id': _('Part Name'),
        }
        widgets = {
            'part_id': forms.Select(attrs={
                'onchange': "Dajaxice.Work.get_part(Dajax.process,{"
                            "'pk': this.value"
                            "});",
                'class': 'form-control',
            }),
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


# endregion

# region Jobs


class JobForm(forms.ModelForm):
    job_address = forms.ModelChoiceField(queryset=Address.objects.all(),
                                         widget=forms.HiddenInput())

    class Meta:
        model = Job
        fields = ['name', 'job_client', 'job_address', 'job_employee']

        widgets = {
            'job_client': forms.Select(attrs={
                'class': 'form-control',
                'onchange': "Dajaxice.Work.get_sites(Dajax.process,{"
                            "'pk': this.value"
                            "});",
            }),
        }
        labels = {
            'name': _('Job Name'),
            'job_client': _('Client Name'),
            'job_address': _('Job Locations'),
            'job_employee': _('Employees on Job'),
        }


class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['building_owner', 'job_client', 'job_address']

# endregion

# region Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['notes', 'ticket_contact']

        widgets = {
            'scheduled_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd",}),
            'scheduled_time': forms.TimeInput,
            'start_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'start_time': forms.TimeInput,
            'end_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'end_time': forms.TimeInput,
            'is_ticket_complete': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'ticket_job': forms.Select(attrs={
                'class': 'form-control'}),
            'ticket_system': forms.Select(attrs={
                'class': 'form-control'}),
            'description_work': forms.Textarea(attrs={
                'cols': 160, 'rows': 5,
                'maxlength': Ticket._meta.get_field(
                'description_work').max_length,
                'onkeyup': "charRemaining('id_description_work', "
                      "'remaining_span')"
            }),
        }
        labels = {
        }
# endregion
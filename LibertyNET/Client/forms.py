from django import forms
from django.utils.translation import gettext as _
from models import Client, SalesProspect, ClientCallLog, SalesProspectCallLog
from Common.forms import AddressForm

#region ClientForms


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['client_address', 'client_contact', 'client_billing']
        help_texts = {
            'business_name': _('Optional.'),
            'is_business': _('Select for commercial accounts.'),
        }
        widgets = {
            'client_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'is_business': forms.CheckboxInput(attrs={
                'class': "iButton-icons"
            })
        }


class ClientForm2(forms.ModelForm):
    client_address = AddressForm()

    class Meta:
        model = Client
        exclude = ['client_contact', 'client_billing']
        fields = [
            'client_number',
            'business_name',
            'is_business',
            'client_address',
            'client_contact',
            'client_billing',
            'client_date',
            'first_name',
            'last_name',
            'middle_initial',
        ]
        help_texts = {
            'business_name': _('Optional.'),
            'is_business': _('Select for commercial accounts.'),
        }
        widgets = {
            'client_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'is_business': forms.CheckboxInput(attrs={
                'class': "iButton-icons"
            })
        }


#endregion

#region SalesProspectForms


class SalesProspectForm(forms.ModelForm):
    class Meta:
        model = SalesProspect
        exclude = ['sp_address', 'sp_contact', 'is_client']

        help_texts = {
            'is_business': _('Select for commercial accounts.'),
        }
        labels = {
            'sp_business_name': _('Business Name'),
        }
        widgets = {
            'initial_contact_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'is_business': forms.CheckboxInput(attrs={
                'class': "iButton-icons"
            })
        }


class SalesProspectEditForm(forms.ModelForm):
    class Meta:
        model = SalesProspect
        exclude = ['sp_address', 'sp_contact']

        help_texts = {
            'is_business': _('Select for commercial accounts.'),
            'is_client': _('Select to convert to Client.'),
        }
        labels = {
            'sp_business_name': _('Business Name'),
        }
        widgets = {
            'initial_contact_date': forms.DateInput(attrs={
                'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'is_business': forms.CheckboxInput(attrs={
                'class': "iButton-icons"
            })
        }


#endregion

#region CallLogForms


class ClientCallLogForm(forms.ModelForm):
    class Meta:
        model = ClientCallLog
        fields = ['client_id', 'caller', 'call_date', 'call_time', 'follow_up',
                  'purpose', 'notes', 'next_contact']
        #exclude = ['client_id']
        widgets = {
            'call_date': forms.DateInput(
                attrs={'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd", 'auto-close': 'true'}),
            'next_contact': forms.DateInput(
                attrs={'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd", 'auto-close': 'true'}),
            'purpose': forms.Textarea(attrs={'cols': 160, 'rows': 3,
                                             'maxlength': ClientCallLog._meta.get_field('purpose').max_length,
                                             'onkeyup': "charRemaining('id_purpose', 'purpose_span')",
                                             # 'onload': "initialChar('id_purpose', 'purpose_span')",
            }),
            'notes': forms.Textarea(attrs={'cols': 160, 'rows': 10,
                                           'maxlength': ClientCallLog._meta.get_field('notes').max_length,
                                           'onkeyup': "charRemaining('id_notes', 'notes_span')",
                                           # 'onload': "initialChar('id_notes', 'notes_span')",
            }),
            'follow_up': forms.CheckboxInput(attrs={'class': "iButton-icons"}),
        }
        labels = {
            'call_date': _('Date of Call'),
            'call_time': _('Time of Call'),
            'follow_up': _('Follow Up Required'),
        }


class SalesProspectCallLogForm(forms.ModelForm):
    class Meta:
        model = SalesProspectCallLog
        fields = ['sales_id', 'caller', 'call_date', 'call_time', 'follow_up',
                  'purpose', 'notes', 'next_contact']

        labels = {
            'call_date': _('Date of Call'),
            'call_time': _('Time of Call'),
            'follow_up': _('Follow Up Required'),
            'sales_id': _('Sales Lead')
        }
        widgets = {
            'call_date': forms.DateInput(attrs={'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'next_contact': forms.DateInput(attrs={'class': 'datepicker fill-up', 'data-date-format': "yyyy-mm-dd"}),
            'purpose': forms.Textarea(attrs={'cols': 160, 'rows': 3,
                                             'maxlength': SalesProspectCallLog._meta.get_field('purpose').max_length,
                                             'onkeyup': "charRemaining('id_purpose', 'purpose_span')",
                                             # 'onload': "initialChar('id_purpose', 'purpose_span')",
            }),
            'notes': forms.Textarea(attrs={'cols': 160, 'rows': 10,
                                           'maxlength': SalesProspectCallLog._meta.get_field('notes').max_length,
                                           'onkeyup': "charRemaining('id_notes', 'notes_span')",
                                           # 'onload': "initialChar('id_notes', 'notes_span')",
            }),
        }

#endregion

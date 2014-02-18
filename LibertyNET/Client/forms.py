from django import forms
from django.utils.translation import gettext as _
from models import Client, SalesProspect, ClientCallLog, SalesProspectCallLog
from bootstrap_toolkit.widgets import BootstrapDateInput

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
            'client_date': BootstrapDateInput,
        }

#endregion

#region SalesProspectForms


class SalesProspectForm(forms.ModelForm):
    class Meta:
        model = SalesProspect
        exclude = ['sp_address', 'sp_contact', 'is_client']
        widgets = {
            'initial_contact_date': BootstrapDateInput,
        }
        help_texts = {
            'is_business': _('Select for commercial accounts.'),
        }
        labels = {
            'sp_business_name': _('Business Name'),
        }


class SalesProspectEditForm(forms.ModelForm):
    class Meta:
        model = SalesProspect
        exclude = ['sp_address', 'sp_contact']
        widgets = {
            'initial_contact_date': BootstrapDateInput,
        }
        help_texts = {
            'is_business': _('Select for commercial accounts.'),
            'is_client': _('Select to convert to Client.'),
        }
        labels = {
            'sp_business_name': _('Business Name'),
        }

#endregion

#region CallLogForms


class ClientCallLogForm(forms.ModelForm):
    class Meta:
        model = ClientCallLog
        exclude = ['client_id']
        widgets = {
            'call_date': BootstrapDateInput,
            'next_contact': BootstrapDateInput,
        }
        labels = {
            'call_date': _('Date of Call'),
            'call_time': _('Time of Call'),
        }


class SalesProspectCallLogForm(forms.ModelForm):
    class Meta:
        model = SalesProspectCallLog
        exclude = ['sales_id']
        widgets = {
            'call_date': BootstrapDateInput,
            'next_contact': BootstrapDateInput,
        }
        labels = {
            'call_date': _('Date of Call'),
            'call_time': _('Time of Call'),
        }

#endregion

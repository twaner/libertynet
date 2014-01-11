from django import forms
from models import Client, Sales_Prospect
from bootstrap_toolkit.widgets import BootstrapDateInput

#region ClientForms


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['client_address', 'client_contact', 'client_billing']
        help_texts = {
            'is_business': _('Select for commercial accounts.'),
        }
        widgets = {
            'client_date': BootstrapDateInput,
        }

#endregion

#region SalesProspectForms


class SalesProspectForm(forms.ModelForm):
    class Meta:
        model = Sales_Prospect
        exclude = ['sp_address', 'sp_contact']
        help_texts = {
            'is_client': _('Select to convert to a Client.')
        }
        widgets = {
            'initial_contact_date': BootstrapDateInput,
        }


#endregion

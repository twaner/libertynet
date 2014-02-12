from django import forms
from django.utils.translation import gettext as _
from models import Client, SalesProspect
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

"""
        def clean(self):
            cleaned_data = Client.clean()
            is_business = boolean_helper(cleaned_data.get('is_business'))
            business_name = cleaned_data.get('business_name')
            first_name = cleaned_data.get('first_name')
            print("SUPERCLEAN ==> is_bus////bus_name", is_business, business_name)
            if first_name != 'Terry':
                raise forms.ValidationError('First name is not terry')

            if is_business and business_name == '':
                print('is_business and not business_name:')
                raise forms.ValidationError("You need to enter a "
                                            "business name")

            elif not is_business and business_name != '':
                print('is_business and business_name:')
                raise forms.ValidationError('Please select \'Is Business\'')
            return cleaned_data
"""

"""msg = u"You mus enter a business name."
                self._errors["business_name"] = self.error_class([msg])"""
"""
help_texts = {
            'is_client': _('Select to convert to a Client.')
        }
"""
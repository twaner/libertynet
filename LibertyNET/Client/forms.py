from django import forms
from django.utils.translation import gettext as _
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
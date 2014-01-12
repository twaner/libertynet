from django import forms
from models import Address, Billing, Contact, Call_List, Installer

#region AddressForms


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'street': _('Street Address'),
            'unit': _('Unit Number'),
        }
        help_texts = {
            'street': _('Ex. 44 Broadway, 4 W. Downs St.'),
            'unit': _('Ex. Apt 23, Unit 4b'),
        }
        error_messages = {
            'zip_code': {
                'max_length': _('Too many digits in Zip Code.'),
            }
        }

#endregion

#region ContactForms


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class EmployeeContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['phone_extension', 'office_phone', 'office_phone_extension',
                   'website']

#endregion

#region BillingForm


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'

#endregion

#region Installer


class Installer(forms.ModelForm):
    class Meta:
        model = Installer
        fields = '__all__'
        widgets = {
            'installer_notes': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
        }


class CallListForm(forms.ModelForm):
    class Meta:
        model = Call_List
        fields = '__all__'

#endregion
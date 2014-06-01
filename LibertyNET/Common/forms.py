from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from models import Address, Billing, Contact, CallList, Installer, Card, UserProfile
from bootstrap_toolkit.widgets import BootstrapDateInput

#region AddressForms


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        labels = dict(street=_('Street Address'), unit=_('Unit Number'))
        help_texts = {
            'street': _('Ex. 44 Broadway'),
            'unit': _('Ex. Apt 23'),
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
        labels = {
            'phone': _('Phone'),
            'phone_extension': _('Phone Ext.'),
            'cell': _('Cell Phone'),
            'office_phone': _('Office Phone'),
            'office_phone_extension': _('Office Ext.'),
        }


class EmployeeContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['phone_extension',
                   'website']
        labels = {
            'phone': _('Phone'),
            'cell': _('Cell Phone'),
            'office_phone': _('Office Phone'),
            'office_phone_extension': _('Office Ext.'),
        }


class CallListContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['cell', 'website', 'email', 'work_email']
        labels = {
            'phone': _('Phone'),
            'phone_extension': _('Phone Ext.'),
        }

#endregion

#region BillingForm


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        exclude = ['billing_address', 'card']
        labels = {
            'profile_name': _('Billing Profile Name'),
            'method': _('Billing Method i.e. Credit Card'),
        }

#endregion

#region CardForm


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        field = '__all__'
        widgets = {
            'card_expiration': BootstrapDateInput,
        }

#endregion

#region Installer


class InstallerForm(forms.ModelForm):
    class Meta:
        model = Installer
        fields = '__all__'
        widgets = {
            'installer_notes': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
        }

#endregion

#region CallListForms


class CallListForm(forms.ModelForm):
    class Meta:
        model = CallList
        exclude = ['cl_contact']
        help_texts = {
            'cl_is_enabled': _('Is call list enabled'),
        }
        labels = {
            'cl_is_enabled': _('Enable Call List'),
            'cl_genre': _('Call List Type'),
            'cl_order': _('Call List Order'),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'eMail'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #fields = '__all__'
        exclude = ['picture', 'user']
        widgets = {
            'first_name': forms.PasswordInput(attrs={'placeholder': 'First Name'}),
            'middle_initial': forms.TextInput(attrs={'placeholder': 'Middle Initial'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }

#endregion
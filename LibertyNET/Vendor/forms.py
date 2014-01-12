from django import forms
from models import Manufacturer, Supplier, Supplier_List

#region ModelForms


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        exclude = ['manu_address', 'manu_contact']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = SupplierForm
        exclude = ['supplier_contact_id']

class SupplierListForm(forms.ModelForm):
    class Meta:
        model = Supplier_List
        fields = '__all__'

#endregion
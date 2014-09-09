from django import forms
from models import Manufacturer, Supplier, SupplierList

#region ModelForms


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        exclude = ['manu_address', 'manu_contact']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['supplier_contact']


class SupplierListForm(forms.ModelForm):
    class Meta:
        model = SupplierList
        fields = '__all__'

#endregion
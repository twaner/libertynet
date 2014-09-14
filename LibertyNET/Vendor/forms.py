from django import forms
from models import Manufacturer, Supplier, SupplierList

#region ModelForms


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        exclude = ['address', 'contact']
        widgets = {
            'is_direct': forms.CheckboxInput(attrs={
                'class': "iButton-icons"
            }),
            'primary_supplier': forms.Select(attrs={
                'class': 'form-control'}),
            'secondary_supplier': forms.Select(attrs={
                'class': 'form-control'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['supplier_contact']
        labels = {
            'supplier_company': 'Company Name:',
            'account': 'Account Number:'
        }


class SupplierListForm(forms.ModelForm):
    class Meta:
        model = SupplierList
        fields = '__all__'

#endregion
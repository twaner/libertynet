import autocomplete_light
from django import forms
from models import Device, Camera, Panel, Part, ClientEstimate, \
    SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales, PartCategory
from Common.helpermethods import readonly_worker

#region EquipmentForms


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = '__all__'


class PartFormEstimate(forms.ModelForm):
    class Meta:
        model = Part
        exclude = ['location', 'quantity']

        widgets = {
            'part_manufacturer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                "class": "form-control"
            }),
            'is_recalled': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'is_active': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'notes': forms.Textarea(attrs={
                'cols': 160, 'rows': 10,
                'maxlength': Part._meta.get_field('notes').max_length,
                'onkeyup': "charRemaining('id_notes', 'notes_span')",
                # 'onload': "initialChar('id_notes', 'notes_span')",
            }),
        }


class PartFormInventory_AC(autocomplete_light.ModelForm):
    class Meta:
        model = Part
        autocomplete_fields = ('name', 'number')
        fields = ['name', 'part_manufacturer', 'number', 'revision', 'quantity',
                  'is_active', 'is_recalled']
        exclude = ['location', 'notes', 'cost', 'flat_price', 'labor', 'spec_sheet', 'install_guide',
                   'category']
        widgets = {
            'is_recalled': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'is_active': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'part_manufacturer': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class PartFormInventory(forms.ModelForm):
    class Meta:
        model = Part

        fields = ['name', 'part_manufacturer', 'number', 'revision', 'quantity',
                  'is_active', 'is_recalled']
        exclude = ['location', 'notes', 'cost', 'flat_price', 'labor', 'spec_sheet', 'install_guide',
                   'category']
        widgets = {
            'is_recalled': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'is_active': forms.CheckboxInput(attrs={
                'class': "iButton-icons"}),
            'part_manufacturer': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class PartFormInventoryRO(PartFormInventory):
    def __init__(self, *args, **kwargs):
        super(PartFormInventoryRO, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            # self.fields['part_manufacturer'].widget.attrs['disabled'] = True
            # print('Part inv %s ' % self.fields['part_manufacturer'].widget)
            # print('Part inv %s ' % type(self.fields['part_manufacturer'].widget))
            field_list = ['name', 'number', 'part_manufacturer', 'revision']
            readonly_worker(self, field_list)

    def clean_part(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.part
        else:
            return self.cleaned_data['part']


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'


class PartCategoryForm(forms.ModelForm):
    class Meta:
        model = PartCategory
        fields = '__all__'


# TODO - Move to Work


class ClientEstimateForm(forms.ModelForm):
    class Meta:
        model = ClientEstimate
        fields = '__all__'


class SalesEstimateForm(forms.ModelForm):
    class Meta:
        model = SalesEstimate
        fields = '__all__'


class EstimatePartsClientForm(forms.ModelForm):
    class Meta:
        model = Estimate_Parts_Client
        fields = '__all__'


class EstimatePartsSalesForm(forms.ModelForm):
    class Meta:
        model = Estimate_Parts_Sales
        fields = '__all__'


        #endregion
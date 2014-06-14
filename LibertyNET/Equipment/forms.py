from django import forms
from models import Device, Camera, Panel, Part, ClientEstimate, \
    SalesEstimate, Estimate_Parts_Client, Estimate_Parts_Sales

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
        exclude = ['location']

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


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'


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
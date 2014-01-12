from django import forms
from models import Equipment, Device, Camera, Panel, Part
#region EquipmentForms


class EquipmentForms(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = '__all__'


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'

        #endregion
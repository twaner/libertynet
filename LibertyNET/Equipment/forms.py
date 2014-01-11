from django import forms
from models import Equipment, Device, Camera, Panel, Part
#region EquipmentForms


class EquipmentForms(forms.ModelForm):
    class Meta:
        model = Equipment


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device


class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel


class PartForm(forms.ModelForm):
    class Meta:
        model = Part


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera

        #endregion
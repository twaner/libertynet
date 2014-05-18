from django import forms
from models import System, Monitoring, Network, Site, Zone

#region ModelForms


class SystemForm(forms.ModelForm):
    class Meta:
        model = System
        fields = '__all__'
        #TODO examine properties


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = '__all__'


class MonitoringForm(forms.ModelForm):
    class Meta:
        model = Monitoring
        fields = '__all__'


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        exclude = ['site_address', 'site_call_list']


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'

#endregion


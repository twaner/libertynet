from django.db import models

#region Models

class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_client = models.ForeignKey('Common.Client')

class System(models.Model):
    system_id = models.AutoField(primary_key=True)
    # System must be at a Site
    system_site = models.ForeignKey('Site.Site')
    system_name = models.CharField(max_length=45)
    system_client_id = models.ForeignKey('Client.Client')
    system_type_id = models.ForeignKey('Equipment.Type')
    system_panel_id = models.ForeignKey('Equipment.Panel', blank=True, null=True)
    tampered_id = models.IntegerField(max_length=11)
    is_system_local = models.BooleanField(default=False)
    panel_location = models.CharField(max_length=45)
    primary_power_location = models.CharField(max_length=45)
    primary_communications = models.IntegerField(max_length=11)
    secondary_communications = models.IntegerField(max_length=11)
    backup_communications = models.IntegerField(max_length=11)
    #TODO ==> Should this be Installer and we get code from Installer Model => nullable
    system_installer_code = models.ForeignKey('Common.Installer_Code', null=True, blank=True)
    master_code = models.IntegerField(max_length=11)
    lockout_code = models.IntegerField(max_length=11)
    #TODO make a common Network Model
    #TODO move to network
    system_ip_address = models.GenericIPAddressField()
    port = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    #TODO is this a FK? to a network model
    network_id = models.ForeignKey('Site.Network')

    #TODO ==> _unicode_

class Network(models.Model):
    network_id = models.AutoField(primary_key=True)
    network_name = models.CharField(max_length=45)
    #TODO ==> Can we use this field instead of VarChar()??
    # https://docs.djangoproject.com/en/1.6/ref/models/fields/#ipaddressfield
    router_address = models.GenericIPAddressField()
    #TODO How to Handle sensitive information?? Salt??
    router_user_name = models.CharField(max_length=45)
    router_password = models.CharField(max_length=45)
    wifi_name = models.CharField(max_length=45)
    wifi_password = models.CharField(max_length=45)
    wifi_notes = models.CharField(max_length=45)

    #TODO _unicode_

class Zone(models.Model):
    zone_id = models.AutoField(primary_key=True)
    system_id = models.ForeignKey('Site.System')
    zone_name = models.CharField(max_length=45)
    zone_location = models.CharField(max_length=45)
    zone_notes = models.CharField(max_length=100)
    is_wireless = models.BooleanField(default=False)

    #TODO _unicode_


class Monitoring(models.Model):
    """
     A Systems monitoring account.
    """
    monitoring_id = models.AutoField(primary_key=True)
    mon_system_id = models.ForeignKey('Site.System')
    #TODO ==> Model for company
    mon_company = models.IntegerField(max_length=11)
    receiver_number = models.IntegerField(max_length=11)
#endregion

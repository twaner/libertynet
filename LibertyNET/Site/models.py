from django.db import models
from Common.models import CallList
from django.core.exceptions import ValidationError

#region ModelManagers


class SiteManager(models.Manager):

    def create_client_site(self, site_client):
        """
        Creates a site with only a client.
        @param site_client: Client related to site.
        @return: Site.
        """
        site = self.create(site_client=site_client)
        site.save()
        return site


class SystemManager(models.Manager):
    def create_system(self, system_site, system_name, system_client_id, system_type_id, system_panel_id,
                      tampered_id, is_system_local, panel_location, primary_power_location,
                      primary_communications, secondary_communications, backup_communications,
                      system_installer_code, master_code, lockout_code, system_ip_address, port,
                      user_name, password, network_id):
        """
        Creates a new system.
        @rtype : System
        @param system_site: Site where System is located.
        @param system_name: Name of system.
        @param system_client_id: Client Id.
        @param system_type_id: System Type Id.
        @param system_panel_id: Panel Id.
        @param tampered_id: Tampered Id.
        @param is_system_local: Is Local?
        @param panel_location: Location of Panel.
        @param primary_power_location: Location of primary power source.
        @param primary_communications: Primary communications.
        @param secondary_communications: Location of secondary power source.
        @param backup_communications: Backup communications.
        @param system_installer_code: Installer's Code.
        @param master_code: Master code.
        @param lockout_code: Lockout code.
        @param system_ip_address: Ip Address.
        @param port: Port.
        @param user_name: Username.
        @param password: Password.
        @param network_id: Network Id.
        @return: System.
        """
        system = self.create(system_site=system_site, system_name=system_name, system_client_id=system_client_id,
                             system_type_id=system_type_id, system_panel_id=system_panel_id, tampered_id=tampered_id,
                             is_system_local=is_system_local, panel_location=panel_location,
                             primary_power_location=primary_power_location,
                             primary_communications=primary_communications,
                             secondary_communications=secondary_communications,
                             backup_communications=backup_communications,
                             system_installer_code=system_installer_code, master_code=master_code,
                             lockout_code=lockout_code,
                             system_ip_address=system_ip_address, port=port, user_name=user_name, password=password,
                             network_id=network_id)
        system.save()
        return system


class NetworkManager(models.Manager):
    def create_network(self, network_name, router_address, router_user_name,
                       router_password, wifi_name, wifi_password, wifi_notes):
        """

        @rtype : Network.
        """
        network = self.create(network_name=network_name, router_address=router_address,
                              router_user_name=router_user_name,
                              router_password=router_password, wifi_name=wifi_name,
                              wifi_password=wifi_password, wifi_notes=wifi_notes)
        network.save()
        return network


class ZoneManager(models.Manager):
    def create_zone(self, system_id, zone_name, zone_location, zone_notes,
                    is_wireless):
        zone = self.create(system_id=system_id, zone_name=zone_name,
                           zone_location=zone_location, zone_notes=zone_notes,
                           is_wireless=is_wireless)
        zone.save()
        return zone


class MonitoringManager(models.Manager):
    def create_monitoring(self, mon_system_id, mon_company, receiver_number):
        monitoring = self.create(mon_system_id=mon_system_id, mon_company=mon_company,
                                 receiver_number=receiver_number)
        monitoring.save()
        return monitoring

#endregion

#region Models


class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_client = models.ForeignKey('Client.Client')
    site_call_list = models.ManyToManyField('Common.CallList', blank=True, null=True)

    objects = SiteManager()

    def __str__(self):
        return '%s' % self.site_client


class System(models.Model):
    system_id = models.AutoField(primary_key=True)
    # System must be at a Site
    system_site = models.ForeignKey('Site.Site')
    system_name = models.CharField(max_length=45)
    system_client_id = models.ForeignKey('Client.Client')
    system_type_id = models.ForeignKey('Common.Genre')
    system_panel_id = models.ForeignKey('Equipment.Panel', blank=True, null=True)
    tampered_id = models.IntegerField(max_length=11)
    is_system_local = models.BooleanField(default=False)
    panel_location = models.CharField(max_length=45)
    primary_power_location = models.CharField(max_length=45)
    primary_communications = models.IntegerField(max_length=11)
    secondary_communications = models.IntegerField(max_length=11)
    backup_communications = models.IntegerField(max_length=11)
    #TODO ==> Should this be Installer and we get code from Installer Model => nullable
    system_installer_code = models.ForeignKey('Common.Installer', null=True, blank=True)
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

    objects = SystemManager()

    def __str__(self):
        return '%s' % self.system_name


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

    objects = NetworkManager()

    def __str__(self):
        return '%s' % self.network_name


class Zone(models.Model):
    zone_id = models.AutoField(primary_key=True)
    system_id = models.ForeignKey('Site.System')
    zone_name = models.CharField(max_length=45)
    zone_location = models.CharField(max_length=45)
    zone_notes = models.CharField(max_length=100)
    is_wireless = models.BooleanField(default=False)

    objects = ZoneManager()

    def __str__(self):
        return '%s %s' % (self.zone_location, self.zone_name)


class Monitoring(models.Model):
    """
     A Systems monitoring account.
    """
    monitoring_id = models.AutoField(primary_key=True)
    mon_system_id = models.ForeignKey('Site.System')
    #TODO ==> Model for company
    mon_company = models.IntegerField(max_length=11)
    receiver_number = models.IntegerField(max_length=11)

    objects = MonitoringManager()

    def __str__(self):
        return 'Monitoring %s' % self.mon_company

#endregion

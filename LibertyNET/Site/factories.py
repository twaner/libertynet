import factory
import factory.fuzzy
from Site.models import Site, Network, Zone, System, Monitoring
import Common.factories as comF
from Common.models import Call_List
import Client.factories as cF
import Equipment.factories as eQF


class SiteFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Site
    site_id = 999
    site_client = factory.SubFactory(cF.ClientFactory)

    @factory.post_generation
    def add_call_list(self, create, extracted, **kwargs):
        """
        Adds Call_List as m2m
        @param create: create.
        @param extracted: extracted.
        @param kwargs: kwargs.
        """
        if extracted and type(extracted) == type(Call_List.objects.all()):
            self.site_call_list = extracted
            self.save()
        else:
            if Call_List.objects.all().count() < 1:
                comF.Call_ListFactory.create()
            [self.site_call_list.add(sc) for sc in Call_List.objects.all()]


class NetworkFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Network
    network_id = 987
    router_address = '192.168.90.6969'
    router_user_name = 'Smith'
    router_password = 'secret'
    wifi_name = 'smithwifi'
    wifi_password = 'secretwifi'
    wifi_notes = 'wifi notes'


class SystemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = System
    system_id = 4567
    system_site = factory.SubFactory(SiteFactory)
    system_name = 'Burg System'
    system_client_id = factory.SubFactory(cF.ClientFactory)
    system_type_id = factory.SubFactory(comF.Genre)
    system_panel_id = factory.SubFactory(eQF.PanelFactory)
    tampered_id = '6868'
    is_system_local = True
    panel_location = 'Front Door'
    primary_power_location = 'Panel primary'
    primary_communications = 'Communications primary'
    secondary_communications = 'Communications secondary'
    backup_communications = 'Communication backup'
    system_installer_code = factory.SubFactory(comF.InstallerFactory)
    master_code = '1234'
    lockout_code = '2345'
    system_ip_address = '192.168.90.1234'
    port = '6666'
    user_name = 'systemusername'
    password = 'systempassword'
    network_id = factory.SubFactory(NetworkFactory)


class ZoneFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Zone
    zone_id = 5434
    system_id = factory.SubFactory(SystemFactory)
    zone_name = 'Front'
    zone_location = 'Front Door'
    zone_notes = 'Located on left of front door'
    is_wireless = True


class MonitoringFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Monitoring
    monitoring_id = 3453
    mon_system_id = factory.SubFactory(SystemFactory)
    mon_company = 'Liberty Security'
    receiver_number = '676767'
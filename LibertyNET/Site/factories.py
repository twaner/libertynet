import factory
import factory.fuzzy
from Site.models import Site, Network, Zone, System, Monitoring
import Common.factories as comf
from Common.models import CallList
import Client.factories as cf
#from Equipment.factories import PanelFactory


class SiteFactoryId(factory.DjangoModelFactory):
    FACTORY_FOR = Site
    site_id = 9898
    site_client = factory.SubFactory(cf.ClientFactory)

    @factory.post_generation
    def add_call_list(self, create, extracted, **kwargs):
        """
        Adds Call_List as m2m
        @param create: create.
        @param extracted: extracted.
        @param kwargs: kwargs.
        """
        if extracted and type(extracted) == type(CallList.objects.all()):
            self.site_call_list = extracted
            self.save()
        else:
            if CallList.objects.all().count() < 1:
                comf.Call_ListFactory.create()
            [self.site_call_list.add(sc) for sc in CallList.objects.all()]


class SiteFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Site
    site_id = factory.Sequence(lambda n: '%04d' % n, type=int)
    site_client = factory.SubFactory(cf.ClientFactory)

    @factory.post_generation
    def add_call_list(self, create, extracted, **kwargs):
        """
        Adds Call_List as m2m
        @param create: create.
        @param extracted: extracted.
        @param kwargs: kwargs.
        """
        if extracted and type(extracted) == type(CallList.objects.all()):
            self.site_call_list = extracted
            self.save()
        else:
            if CallList.objects.all().count() < 1:
                comf.Call_ListFactory.create()
            [self.site_call_list.add(sc) for sc in CallList.objects.all()]


class NetworkFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Network
    network_id = factory.Sequence(lambda n: '%04d' % n, type=int)
    router_address = '192.168.90.6969'
    router_user_name = 'Smith'
    router_password = 'secret'
    wifi_name = 'smithwifi'
    wifi_password = 'secretwifi'
    wifi_notes = 'wifi notes'


class SystemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = System
    system_id = factory.Sequence(lambda n: '%04d' % n, type=int)
    system_site = factory.SubFactory(SiteFactory)
    system_name = 'Burg System'
    system_client_id = factory.SubFactory(cf.ClientFactory)
    system_type_id = factory.SubFactory(comf.GenreFactory)
    system_panel_id = factory.SubFactory('Equipment.factories.PanelFactory')
    tampered_id = '6868'
    is_system_local = True
    panel_location = 'Front Door'
    primary_power_location = 'Panel primary'
    primary_communications = factory.sequence(lambda n: "%33d" % n)
    secondary_communications = factory.sequence(lambda n: "%44d" % n)
    backup_communications = factory.sequence(lambda n: "%55d" % n)
    system_installer_code = factory.SubFactory(comf.InstallerFactory)
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
    mon_company = 9494
    receiver_number = '676767'
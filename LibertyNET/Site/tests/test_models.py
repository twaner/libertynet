from django.test import TestCase
import Site.factories as sf
from Site.models import Site, Network, Zone, System, Monitoring
from Common.models import Address, Contact
import Common.factories as cf
from Common.helpermethods import assert_equals_worker, assert_true_worker
from Client.factories import ClientFactory
import Equipment.factories as ef

#region Globals

add = {'id': '1818', 'street': '44 Broadway', 'unit': '4B', 'city': 'Kingston', 'state': 'New York',
       'zip_code': '12401'}

con = {'id': '2020', 'phone': '8453334444', 'phone_extension': '44', 'cell': '8456667777', 'office_phone': '9998883333',
       'office_phone_extension': '4545', 'email': 'test@test.com', 'work_email': 'work@work.com',
       'website': 'www.test.com'}

#endregion

#region Factory Tests


class FactoryTestCases(TestCase):
    print('Starting SiteFactoryTestCases...')

    def test_site_factory(self):
        site = sf.SiteFactory()
        self.assertTrue(isinstance(site, Site), "SiteFactory is not Site")

    def test_system_factory(self):
        system = sf.SystemFactory()
        self.assertTrue(isinstance(system, System), 'SystemFactory is not System')

    def test_site_factory_two(self):
        site = sf.SiteFactory()
        self.assertTrue(isinstance(site, Site), "SiteFactory is not Site")
        self.assertEqual(site.site_call_list.count(), 1, 'SiteFactory call_list count not 1')

    def test_network_factory(self):
        network = sf.NetworkFactory()
        self.assertTrue(isinstance(network, Network), 'NetworkFactory is not Network')

    def test_zone_factory(self):
        zone = sf.ZoneFactory()
        self.assertTrue(isinstance(zone, Zone), 'ZoneFactory is not Zone')

    def test_monitoring_factory(self):
        monitoring = sf.MonitoringFactory()
        self.assertTrue(isinstance(monitoring, Monitoring), 'MonitoringFactory is not Monitoring')


#endregion

#region Model Tests


class TestSite(TestCase):
    def setUp(self):
        """
        Setup for test class.
        """
        a = Address.objects.create(id=add['id'], street=add['street'], unit=add['unit'],
                                   city=add['city'], state=add['state'], zip_code=add['zip_code'])
        c = Contact.objects.create(id=con['id'], phone=con['phone'], phone_extension=con['office_phone_extension'],
                                   cell=con['cell'], office_phone=con['office_phone'], email=con['email'],
                                   work_email=con['work_email'])
        self.assertTrue(isinstance(a, Address), "Address not created")
        self.assertTrue(isinstance(c, Contact), "Contact not created.")

    def test_create_site(self):
        """
        Test Site object.
        """
        client = ClientFactory()
        site = Site.objects.create_client_site(site_client=client)
        self.assertTrue(isinstance(site, Site), 'site is not Site')
        pk = site.site_id

        # CallLists Tests
        calllist = cf.Call_ListFactory()
        site.site_call_list.add(calllist)
        assert_equals_worker(self, 1, site.site_call_list.count())
        calllist2 = cf.Call_ListFactory()
        site.site_call_list.add(calllist2)
        assert_equals_worker(self, 2, site.site_call_list.count())

        # Test get_absoulte_url
        abs_url_str = '/client/sitedetails/%s/' % pk
        abs_url_edit_str = '/client/addclientcalllist/%s/' % pk

        assert_equals_worker(self, abs_url_str, site.get_absolute_url_())
        assert_equals_worker(self, abs_url_edit_str, site.get_absolute_url_add_calllist())

class TestModels(TestCase):
    def setUp(self):
        """
        Setups for test. Creates a System for use with other tests.
        """
        factory_system = sf.SystemFactory()
        self.assertTrue(isinstance(factory_system, System), 'system is Not System')
        client = ClientFactory()
        site = Site.objects.create_client_site(site_client=client)
        genre = cf.GenreFactory()
        sys_inst_code = cf.InstallerFactory()
        panel = ef.PanelFactory()
        network = sf.NetworkFactory()
        self.assertTrue(isinstance(site, Site), 'site is not Site')
        system = System.objects.create_system(system_site=site, system_name='system name', system_client_id=client,
                                              system_panel_id=panel, tampered_id='69', is_system_local=True,
                                              system_type_id=genre, panel_location='panel location',
                                              primary_power_location='primary pwr loc',
                                              primary_communications='5555', secondary_communications='6666',
                                              backup_communications='7777', system_installer_code=sys_inst_code,
                                              master_code='8888', lockout_code='9999', system_ip_address='192.168.1.22',
                                              port='9001', user_name='sys user name', password='syspw',
                                              network_id=network)
        self.assertTrue(isinstance(system, System), 'system is not System')
        assert_equals_worker(self, system.system_name, system.__str__())

    def test_create_zone(self):
        """
        Tests creation of a Zone.
        """
        system = System.objects.get(tampered_id='69')
        zone = Zone.objects.create_zone(system, 'zone name', 'zone location', 'zone notes', True)
        self.assertTrue(isinstance(zone, Zone), 'zone is not Zone')
        assert_equals_worker(self, ('%s %s' % (zone.zone_location, zone.zone_name)), zone.__str__())

    def test_create_monitoring(self):
        """
        Tests creation of a Monitoring object.
        """
        system = System.objects.get(system_name='Burg System')
        monitoring = Monitoring.objects.create_monitoring(system, 1111, 2222)
        self.assertTrue(isinstance(monitoring, Monitoring), 'monitoring is not Monitoring')
        self.assertEqual(monitoring.__str__(), 'Monitoring 1111', 'monitoring__str__() wrong')

    def test_network(self):
        """
        Tests creation of a Network object.

        """
        network = Network.objects.create_network('network name', '192.168.88.123', 'router user name', 'routerpw',
                                                 'wifiname', 'wifipw', 'wifi notes')

        self.assertTrue(isinstance(network, Network), 'network is not Network')
        assert_equals_worker(self, network.network_name, network.__str__())

#endregion
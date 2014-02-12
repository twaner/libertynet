from django.test import TestCase
import Site.factories as sf
from Site.models import Site, Network, Zone, System, Monitoring

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



#endregion
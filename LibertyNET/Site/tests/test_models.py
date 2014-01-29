from django.test import TestCase
import Site.factories as sF
from Site.models import Site

#region Factory Tests


class FactoryTestCases(TestCase):
    def test_site_factory(self):
        site = sF.SiteFactory()
        self.assertTrue(isinstance(site, Site), "SiteFactory is not Site")

    def test_site_factory_two(self):
        site = sF.SiteFactory()
        self.assertTrue(isinstance(site, Site), "SiteFactory is not Site")
        self.assertEqual(site.site_call_list.count(), 1, 'SiteFactory call_list count not 1')



#endregion

#region Model Tests



#endregion
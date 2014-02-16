from django.test import TestCase
from django.core.urlresolvers import reverse
from Site.factories import SiteFactoryId
from Site.models import Site
from Common.helpermethods import assert_equals_worker, assert_in_worker
from Client.models import Client

#region ViewTests


class TestSiteDetailView(TestCase):
    def setUp(self):
        site = SiteFactoryId()
        self.assertTrue(isinstance(site, Site))

    def test_site_detail_view(self):
        site = Site.objects.get(pk=9898)
        client = Client.objects.get(pk=site.site_client_id)
        url = reverse('Client:sitedetails', kwargs={'pk': site.site_id})
        resp = self.client.get(url)
        mycall = site.site_call_list.all()[0]

        assert_equals_worker(self, resp.status_code, 200)
        assert_in_worker(self, client.first_name, resp.content)
        assert_in_worker(self, client.client_address.street, resp.content)
        assert_in_worker(self, str(mycall.cl_order), resp.content)

#endregion
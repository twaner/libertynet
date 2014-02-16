from django.test import TestCase
from django.core.urlresolvers import reverse
import Common.factories as cf
import Client.factories as clf
from Client.models import Client
from Common.helpermethods import assert_equals_worker, assert_in_worker
from Common.models import Billing, CallList
from Site.factories import SiteFactory


class TestCommonViews(TestCase):
    def setUp(self):
        client = clf.ClientFactory()
        self.assertTrue(isinstance(client, Client))
        billing = cf.BillingFactory()
        self.assertTrue(isinstance(billing, Billing))
        calllist = cf.Call_ListFactory()
        self.assertTrue(isinstance(calllist, CallList))

    def test_add_client_billing_view(self):
        cl = Client.objects.get(first_name='Stephen')
        url = reverse('Client:addclientbilling', kwargs={'pk': cl.client_id})
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)

    def test_edit_client_billing(self):
        cl = Client.objects.get(first_name='Stephen')
        b = Billing.objects.get(id=cl.client_billing_id)
        url = reverse('Client:editclientbilling', kwargs={'pk': b.id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, b.profile_name, resp.content)
        assert_in_worker(self, b.billing_address.street, resp.content)
        assert_in_worker(self, b.card.first_name, resp.content)

    def test_call_list_details_views(self):
        cl = CallList.objects.get(first_name='Jason')
        url = reverse('Client:calllistdetails', kwargs={'pk': cl.call_list_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, str(cl.cl_order), resp.content)
        assert_in_worker(self, cl.cl_contact.__str__(), resp.content)

    def test_add_call_list(self):
        s = SiteFactory()
        url = reverse('Client:addclientcalllist', kwargs={'pk': s.site_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)

    def test_update_call_list(self):
        site = SiteFactory()
        cl = site.site_call_list.filter(first_name='Jason')[0]
        url = reverse('Client:editclientcalllist', kwargs={'pk': cl.call_list_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, cl.first_name, resp.content)
        assert_in_worker(self, cl.cl_contact.phone, resp.content)


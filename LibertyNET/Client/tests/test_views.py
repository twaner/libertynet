from django.test import TestCase
from django.core.urlresolvers import reverse
from Client.models import Client, SalesProspect, ClientCallLog, SalesProspectCallLog
import Client.factories as cf
from Common.helpermethods import assert_equals_worker, assert_in_worker


#region ClientViewTests


class ClientViewTest(TestCase):
    def setUp(self):
        cl = cf.ClientFactory()
        call_log = cf.ClientCallLogFactory(client_id=cl)

    def test_client_list_view(self):
        cl = Client.objects.get(first_name='Stephen')
        url = reverse('Client:index')
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, cl.first_name, resp.content)

    def test_client_details_view(self):
        cl = Client.objects.get(first_name='Stephen')
        url = reverse('Client:details', kwargs={'pk': cl.client_id})
        resp = self.client.get(url)

        assert_equals_worker(self, resp.status_code, 200)
        assert_in_worker(self, cl.first_name, resp.content)
        assert_in_worker(self, cl.client_address.street, resp.content)
        assert_in_worker(self, cl.client_contact.__str__(), resp.content)

    def test_add_client_view(self):
        url = reverse('Client:addclient')
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)

    def test_edit_client_view(self):
        cl = Client.objects.get(first_name='Stephen')
        url = reverse('Client:editclient', kwargs={'pk': cl.client_id})
        resp = self.client.get(url)

        assert_equals_worker(self, resp.status_code, 200)
        assert_in_worker(self, cl.first_name, resp.content)
        assert_in_worker(self, cl.client_address.street, resp.content)
        assert_in_worker(self, cl.client_contact.phone, resp.content)

    # CallLog
    def test_add_client_calllog_view(self):
        cl = Client.objects.get(first_name='Stephen')
        url = reverse('Client:addclientcalllog', kwargs={'pk': cl.client_id})
        resp = self.client.get(url)
        assert_equals_worker(self, resp.status_code, 200)

    def test_client_call_detail_view(self):
        cl = Client.objects.get(first_name='Stephen')
        calllog = ClientCallLog.objects.get(client_id=cl)
        url = reverse('Client:clientcalllogdetails', kwargs={'pk': calllog.id})
        resp = self.client.get(url)
        assert_equals_worker(self, resp.status_code, 200)
        assert_in_worker(self, cl.first_name, resp.content)
        assert_in_worker(self, str(calllog.notes), resp.content)

    def test_client_call_log_index(self):
        cl = Client.objects.get(first_name='Stephen')
        calllog = ClientCallLog.objects.get(client_id=cl.client_id)
        url = reverse('Client:clientcalllogindex', kwargs={'pk': cl.client_id})
        resp = self.client.get(url)
        assert_equals_worker(self, resp.status_code, 200)

    def test_sales_call_home_view(self):
        cl = Client.objects.get(first_name='Stephen')
        calllog = ClientCallLog.objects.get(client_id=cl.client_id)
        url = reverse('Client:callloghome')
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, calllog.complete_details, resp.content)

#endregion

#region SalesProspectViewTest


class TestSalesProspectView(TestCase):
    def setUp(self):
        sp = cf.SalesProspectResidentialFactory()
        sales_call_log = cf.SalesProspectCallLogFactory(sales_id=sp)

    def test_sales_index_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        url = reverse('Client:salesprospectindex')
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, sp.first_name, resp.content)

    def test_sales_detail_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        url = reverse('Client:salesprospectdetails', kwargs={'pk': sp.sales_prospect_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, sp.first_name, resp.content)
        assert_in_worker(self, sp.sp_address.__str__(), resp.content)
        assert_in_worker(self, sp.sp_contact.__str__(), resp.content)

    def test_add_sales_view(self):
        url = reverse('Client:addsalesprospect')
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)

    def test_edit_sales_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        url = reverse('Client:editsalesprospect', kwargs={'pk': sp.sales_prospect_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, sp.first_name, resp.content)
        assert_in_worker(self, sp.sp_address.street, resp.content)
        assert_in_worker(self, sp.sp_contact.phone, resp.content)

    def test_edit_sales_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        url = reverse('Client:salestoclient', kwargs={'pk': sp.sales_prospect_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, sp.first_name, resp.content)
        assert_in_worker(self, sp.sp_address.street, resp.content)
        assert_in_worker(self, sp.sp_contact.phone, resp.content)

    # CallLog
    def test_add_sales_call_log_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        cl = SalesProspectCallLog.objects.get(sales_id=sp.sales_prospect_id)
        url = reverse('Client:salestoclient', kwargs={'pk': sp.sales_prospect_id})
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)

    def test_sales_call_log_detail_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        scl = SalesProspectCallLog.objects.get(sales_id=sp.sales_prospect_id)
        url = reverse('Client:salescalllogdetails', kwargs={'pk': scl.id})
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, scl.notes, resp.content)

    def test_sales_call_log_index(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        scl = SalesProspectCallLog.objects.get(sales_id=sp.sales_prospect_id)
        url = reverse('Client:salescalllogindex', kwargs={'pk': sp.sales_prospect_id})
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, scl.complete_details, resp.content)

    def test_sales_call_home_view(self):
        sp = SalesProspect.objects.get(first_name='Sally')
        scl = SalesProspectCallLog.objects.get(sales_id=sp.sales_prospect_id)
        url = reverse('Client:salescallloghome')
        resp = self.client.get(url)
        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, scl.complete_details, resp.content)
from django.test import TestCase
from datetime import date, timedelta
from Client.models import Client, SalesProspect, ClientCallLog
from Client.factories import *
from Employee.factories import EmployeeFactory
from Common.models import Address, Contact, Card, Billing
from Common.factories import *
import Common.helpermethods as chm

#region Globals


add = {'street': '44 Broadway', 'unit': '4B', 'city': 'Kingston', 'state': 'New York', 'zip_code': '12401'}

con = {'phone': '8453334444', 'cell': '8456667777', 'office_phone': '9998883333', 'office_phone_extension': '4545',
       'email': 'test@test.com', 'work_email': 'work@work.com'}

date1 = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
date2 = (date.today() + timedelta(days=100)).strftime("%Y-%m-%d")

#endregion

#region ClientFactoryTest


class FactoryTests(TestCase):
    def test_create_client_factory(self):
        print('Starting test_create_client_factory...')
        client = ClientFactory()
        self.assertTrue(isinstance(client, Client), "ClientFactory - !Client")
        self.assertTrue(isinstance(client.client_billing, Billing), "ClientFactory - !client_billing")

    def test_create_client_factory_no_billing(self):
        print('Starting test_create_client_factory_no_billing...')
        client = ClientFactoryNoBilling()
        self.assertTrue(isinstance(client, Client), 'ClientFactoryNoBilling !Client')

    def test_create_business_client_factory(self):
        print('Starting test_create_business_client_factory...')
        client = ClientFactoryBusiness()
        self.assertTrue(isinstance(client, Client), "ClientFactoryBusiness - !Client")
        self.assertTrue(client.business_name == 'Clientbusiness', 'Client business name incorrect')
        self.assertEqual(client.is_business, True, 'Client.is_business is not True')

    def test_create_sales_prospect_residential(self):
        print('test_create_sales_prospect_residential...')
        sales_prospect = SalesProspectResidentialFactory()
        self.assertTrue(isinstance(sales_prospect, SalesProspect), 'SalesProspectResidentialFactory !SalesProspect')
        self.assertTrue(isinstance(sales_prospect.sp_address, Address), 'SalesProspect !Address')
        self.assertTrue(isinstance(sales_prospect.sp_contact, Contact), 'SalesProspect !Contact')
        self.assertEqual(sales_prospect.is_business, False, 'SP.is_business !False')
        self.assertEqual(sales_prospect.get_absolute_url(),
                         '/client/salesprospectdetails/999/', 'AbsoluteUrl does not match')
        self.assertEqual(sales_prospect.get_absolute_url_edit(),
                         '/client/editsalesprospect/999/', 'AbsoluteUrl does not match')

    def test_create_sales_prospect_business(self):
        print('test_create_sales_prospect_business...')
        sales_prospect = SalesProspectBusinessFactory()
        self.assertTrue(isinstance(sales_prospect, SalesProspect), 'SalesProspectResidentialFactory !SalesProspect')
        self.assertEqual(sales_prospect.sp_business_name, 'Salesprospectbusiness', 'SP business name is incorrect')
        self.assertEqual(sales_prospect.is_business, True, 'SP.is_business !True')

    def test_client_call_log_factory(self):
        call_log = ClientCallLogFactory()
        self.assertIsInstance(call_log, ClientCallLog)
        str_exp = 'Client: %s Call Date: %s' % (call_log.client_id.__str__(), call_log.call_date)
        chm.assert_equals_worker(self, str_exp, call_log.__str__())
        chm.assert_equals_worker(self, call_log.next_call, call_log.next_call)

    def test_sales_call_log_factory(self):
        call_log = SalesProspectCallLogFactory()
        self.assertIsInstance(call_log, SalesProspectCallLog)
        str_exp = 'Prospect: %s Call Date: %s' % (call_log.sales_id.__str__(), call_log.call_date)
        chm.assert_equals_worker(self, str_exp, call_log.__str__())
        chm.assert_equals_worker(self, call_log.next_call, call_log.next_call)


#endregion

class ClientTest(TestCase):
    def setUp(self):
        print('Starting setup...')
        a = Address.objects.create(id=1111, street='44 Broadway', unit='4B', city='Kingston', state='New York',
                                   zip_code='12401')
        self.assertTrue(isinstance(a, Address), "Address not created")
        c = Contact.objects.create(id=2222, phone='8453334444', cell='8456667777',
                                   office_phone='9998883333', office_phone_extension='4545',
                                   email='test@test.com', work_email='work@work.com')
        self.assertTrue(isinstance(c, Contact), "Contact not created.")
        print('setup completed...')

    def test_create_client(self):
        a = Address.objects.get(pk=1111)
        self.assertTrue(isinstance(a, Address), 'address != Address')
        c = Contact.objects.get(pk=2222)
        self.assertTrue(isinstance(c, Contact), 'contact != Contact')
        client = Client.objects.create_client(first_name='Al', middle_initial='Q', last_name='Alston',
                                              client_number=9191, client_address=a, client_contact=c,
                                              client_date='2013-12-29', is_business=False, business_name='')
        self.assertTrue(isinstance(client, Client), 'client is not Client.')
        #self.assertEqual(client.__str__(), 'Al Q Alston', '__str__ not matching.')
        chm.assert_equals_worker(self, 'Al Q Alston', client.__str__())
        self.assertEqual(client.is_business, False, 'Client.is_business is wrong.')
        chm.assert_equals_worker(self, False, client.is_business)
        #self.assertEqual(client.is_a_business(), False, 'Client is not a business.')
        chm.assert_equals_worker(self, False, client.is_a_business())

        # get_absolute_url
        url = '/client/%s/' % client.client_id
        url_edit = '/client/editclient/%s/' % client.client_id
        url_calllog = '/client/addclientcalllog/%s/' % client.client_id
        url_calllog_index = '/client/clientcalllogindex/%s/' % client.client_id
        chm.assert_equals_worker(self, url, client.get_absolute_url())
        chm.assert_equals_worker(self, url_edit, client.get_absolute_url_edit())
        chm.assert_equals_worker(self, url_calllog, client.get_absolute_url_calllog())
        chm.assert_equals_worker(self, url_calllog_index, client.get_absolute_url_calllog_index())

        # CallLog Tests
        emp = EmployeeFactory()
        calllog = ClientCallLog.objects.create_client_calllog(client, emp, '2014-02-13', '13:13',
                                                              'purpose', 'notes', date1)
        calllog2 = ClientCallLog.objects.create_client_calllog(client, emp, '2014-02-17', '13:13',
                                                               'purpose2', 'notes2', date2)

        calllog_modelmanager = ClientCallLog.objects.get_next_contact_date(client)
        chm.assert_equals_worker(self, date1, calllog_modelmanager.next_call)

        #property tests
        full_details = 'Client: %s Call Date: %s Time: %s' % (calllog.client_id, calllog.call_date, calllog.call_time)
        chm.assert_equals_worker(self, full_details, calllog.full_details)
        complete_details = 'Client: %s Purpose: %s Call Date: %s Time: %s' % (calllog.client_id, calllog.purpose,
                                                                              calllog.call_date, calllog.call_time)
        chm.assert_equals_worker(self, complete_details, calllog.complete_details)

        # get_absolute_url
        exp = '/client/clientcalllogdetails/%s/' % calllog.id
        chm.assert_equals_worker(self, exp, calllog.get_absolute_url())
        url_client = '/client/%s/' % calllog.client_id.client_id
        chm.assert_equals_worker(self, url_client, calllog.get_absolute_url_client())
        url_index = '/client/clientcalllogindex/%s/' % calllog.client_id.client_id
        chm.assert_equals_worker(self, url_index, calllog.get_absolute_url_index())
        url_abs = '/client/clientcalllogdetails/%s/' % calllog.id
        chm.assert_equals_worker_long(self, url_abs, calllog.get_absolute_url(), calllog.get_absolute_url.__name__)


class SalesProspectTest(TestCase):
    def setUp(self):
        print('Starting setup...')
        a = Address.objects.create(id=1111, street='44 Broadway', unit='4B', city='Kingston', state='New York',
                                   zip_code='12401')
        self.assertTrue(isinstance(a, Address), "Address not created")
        c = Contact.objects.create(id=2222, phone='8453334444', cell='8456667777',
                                   office_phone='9998883333', office_phone_extension='4545',
                                   email='test@test.com', work_email='work@work.com')
        self.assertTrue(isinstance(c, Contact), "Contact not created.")
        print('setup completed...')

    def test_create_client(self):
        a = Address.objects.get(pk=1111)
        self.assertTrue(isinstance(a, Address), 'address != Address')
        c = Contact.objects.get(pk=2222)
        self.assertTrue(isinstance(c, Contact), 'contact != Contact')
        lib_emp = EmployeeFactory()
        sp = SalesProspect.objects.create_sales_prospect(first_name="Annie", middle_initial='T', last_name='Bass',
                                                         sp_liberty_contact=lib_emp, sales_type='New',
                                                         sales_probability='Medium', initial_contact_date='2014-3-22',
                                                         comments='None', sp_address=a, sp_contact=c, is_business=False,
                                                         sp_business_name='')

        self.assertTrue(isinstance(sp, SalesProspect), 'sp is not SalesProspect.')
        self.assertEqual(sp.__str__(), 'Annie T Bass', '__str__ not matching.')
        self.assertEqual(sp.is_business, False, 'Client.is_business is wrong.')

        # CallLog
        emp = EmployeeFactory()
        calllog = SalesProspectCallLog.objects.create_sales_calllog(sp, emp, '2014-02-13', '13:13',
                                                                    'purpose', 'notes', date1)
        calllog2 = SalesProspectCallLog.objects.create_sales_calllog(sp, emp, '2014-02-17', '13:13',
                                                                     'purpose2', 'notes2', date2)
        calllog_modelmanager = SalesProspectCallLog.objects.get_next_contact_date(sp)
        chm.assert_equals_worker(self, date1, calllog_modelmanager.next_call)


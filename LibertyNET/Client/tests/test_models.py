from django.test import TestCase
from Client.models import Client, SalesProspect
from Client.factories import *
from Employee.factories import EmployeeFactory
from Common.models import Address, Contact, Card, Billing
from Common.factories import *
import Common.helpermethods as chm

#region Globals


add = {'street': '44 Broadway', 'unit': '4B', 'city': 'Kingston', 'state': 'New York', 'zip_code': '12401'}

con = {'phone': '8453334444', 'cell': '8456667777', 'office_phone': '9998883333', 'office_phone_extension': '4545',
       'email': 'test@test.com', 'work_email': 'work@work.com'}

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
                                              client_date='2013-12-29')
        self.assertTrue(isinstance(client, Client), 'client is not Client.')
        self.assertEqual(client.__str__(), 'Al Q Alston', '__str__ not matching.')
        self.assertEqual(client.is_business, False, 'Client.is_business is wrong.')
        self.assertEqual(client.is_a_business(), False, 'Client is not a business.')


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
                                                         comments='None', sp_address=a, sp_contact=c)
                                                         #is_business=False, is_client=False, sp_business_name='')
        self.assertTrue(isinstance(sp, SalesProspect), 'sp is not SalesProspect.')
        self.assertEqual(sp.__str__(), 'Annie T Bass', '__str__ not matching.')
        self.assertEqual(sp.is_business, False, 'Client.is_business is wrong.')


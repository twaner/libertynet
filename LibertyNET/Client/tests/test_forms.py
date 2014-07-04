from django.test import TestCase
from datetime import date, timedelta
from Client.models import Client, SalesProspect
from Client.factories import *
from Client.forms import ClientForm, SalesProspectForm, SalesProspectEditForm, \
    SalesProspectCallLogForm, ClientCallLogForm
from Common.forms import AddressForm, ContactForm
from Client.factories import SalesProspectResidentialFactory
from Common.models import Address, Contact, Card, Billing
from Common.factories import *
import Common.helpermethods as chm

#region Globals

date1 = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
date2 = (date.today() + timedelta(days=100)).strftime("%Y-%m-%d")
date_today = date.today().strftime("%Y-%m-%d")

#endregion

#region ClientTest Form


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

    def test_client_form(self):
        a = Address.objects.get(pk=1111)
        c = Contact.objects.get(pk=2222)
        client = Client.objects.create_client(first_name='Al', middle_initial='Q', last_name='Alston',
                                              client_number=9191, client_address=a, client_contact=c,
                                              client_date='2013-12-29', is_business=None, business_name=None)
        chm.assert_true_worker(self, Client, client)
        client_data = {
            'first_name': client.first_name, 'middle_initial': client.middle_initial, 'last_name': client.last_name,
            'client_number': client.client_number, 'client_date': client.client_date
        }
        form = ClientForm(data=client_data)
        chm.form_assert_true_worker(self, form)

    def test_invalid_client_form(self):
        client = Client()
        client_data = {
            'first_name': client.first_name, 'middle_initial': client.middle_initial, 'last_name': client.last_name,
            'client_number': client.client_number, 'client_date': client.client_date
        }
        form = ClientForm(data=client_data)
        chm.form_assert_false_worker(self, form)

    def test_create_sales_prospect_residential(self):
        a = Address.objects.get(pk=1111)
        self.assertTrue(isinstance(a, Address), 'address != Address')
        c = Contact.objects.get(pk=2222)
        self.assertTrue(isinstance(c, Contact), 'contact != Contact')
        liberty_contact = EmployeeFactory(employee_id=909900, emp_address=a, emp_contact=c)
        # Sales Prospect
        # sp = SalesProspect.objects.create_sales_prospect(first_name='Ken', middle_initial='L',
        #                                                  last_name='Salesprospect',
        #                                                  sp_liberty_contact=liberty_contact,
        #                                                  sales_type='New', sales_probability='L',
        #                                                  initial_contact_date='2014-1-15', comments='new lead.',
        #                                                  sp_address=a, sp_contact=c)
        sp = SalesProspectBusinessFactory()
        self.assertTrue(isinstance(sp, SalesProspect), 'salesprospect != SalesProspect')
        # Form work
        sales_prospect_data = {
            'first_name': sp.first_name, 'middle_initial': sp.middle_initial, 'last_name': sp.last_name,
            'sp_liberty_contact': sp.sp_liberty_contact_id, 'sales_type': sp.sales_type,
            'sales_probability': sp.sales_probability, 'initial_contact_date': sp.initial_contact_date,
            'comments': sp.comments
        }
        # form work
        form_list = chm.form_generator(1)
        form_list[0] = SalesProspectForm(data=sales_prospect_data)
        # For debugging
        chm.form_errors_printer(form_list)
        # Verify forms are valid
        self.assertTrue(form_list[0].is_valid())

    def test_edit_salesprospect_form(self):
        sp = SalesProspectResidentialFactory()
        sales_prospect_data = {
            'first_name': sp.first_name, 'middle_initial': sp.middle_initial, 'last_name': sp.last_name,
            'sp_liberty_contact': sp.sp_liberty_contact_id, 'sales_type': sp.sales_type,
            'sales_probability': sp.sales_probability, 'initial_contact_date': sp.initial_contact_date,
            'comments': sp.comments, 'service_guide': sp.service_guide
        }
        form = SalesProspectEditForm(data=sales_prospect_data)
        self.assertTrue(form.is_valid(), 'SalesProspectEditForm is not valid!')

    def test_invald_salesprospect_forms(self):
        sp = SalesProspect()
        sales_prospect_data = {
            'first_name': sp.first_name, 'middle_initial': sp.middle_initial, 'last_name': sp.last_name,
            'sp_liberty_contact': sp.sp_liberty_contact_id, 'sales_type': sp.sales_type,
            'sales_probability': sp.sales_probability, 'initial_contact_date': sp.initial_contact_date,
            'comments': sp.comments, 'service_guide': sp.service_guide
        }
        form = SalesProspectEditForm(data=sales_prospect_data)
        chm.form_assert_false_worker(self, form)
        form2 = SalesProspectForm(data=sales_prospect_data)
        chm.form_assert_false_worker(self, form2)

#endregion

#region CallLogFormTest


class TestCallLogForms(TestCase):
    def setUp(self):
        client = ClientFactory()
        sales = SalesProspectBusinessFactory()
        employee = EmployeeFactory()

    def test_client_calllog_form(self):
        client = Client.objects.get(client_number=8989)
        employee = Employee.objects.filter(last_name='Smith').first()
        call_data = {}
        form = ClientCallLogForm()
        chm.form_assert_false_worker(self, form)
        call_data = {
            'client_id': client.client_id, 'caller': employee.employee_id, 'call_date': date1,
            'call_time': '13:13', 'purpose': 'call purpose', 'notes': 'call notes',
            'next_contact': date2, 'follow_up': True
        }
        form = ClientCallLogForm(data=call_data)
        chm.form_errors_printer(form)
        chm.form_assert_true_worker(self, form)

    def test_sales_calllog_form(self):
        sales = SalesProspect.objects.get(id=9901)
        employee = Employee.objects.filter(last_name='Smith').first()
        call_data = {}
        form = SalesProspectCallLogForm()
        chm.form_assert_false_worker(self, form)
        call_data = {
            'caller': employee.employee_id, 'call_date': date1, 'call_time': '13:13',
            'purpose': 'call purpose', 'notes': 'call notes', 'next_contact': date2,
            'follow_up': True
        }
        chm.form_errors_printer(form)
        form = SalesProspectCallLogForm(data=call_data)
        chm.form_assert_true_worker(self, form)

#endregion

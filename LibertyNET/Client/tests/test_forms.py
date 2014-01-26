from django.test import TestCase
from Client.models import Client, Sales_Prospect
from Client.factories import *
from Client.forms import ClientForm, SalesProspectForm
from Common.forms import AddressForm, ContactForm
from Common.models import Address, Contact, Card, Billing
from Common.factories import *
import Common.helpermethods as CHM

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

    def test_create_client(self):
        a = Address.objects.get(pk=1111)
        self.assertTrue(isinstance(a, Address), 'address != Address')
        c = Contact.objects.get(pk=2222)
        self.assertTrue(isinstance(c, Contact), 'contact != Contact')
        client = Client.objects.create_client(first_name='Al', middle_initial='Q', last_name='Alston',
                                              client_number=9191, client_address=a, client_contact=c,
                                              client_date='2013-12-29')
        self.assertTrue(isinstance(client, Client), 'client is not Client')

        #setup for forms
        address_data = {'street': a.street, 'unit': a.unit, 'city': a.city, 'state': a.state,
                        'zip_code': a.zip_code,
        }
        contact_data = {
            'phone': c.phone, 'cell': c.cell, 'office_phone': c.office_phone,
            'office_phone_extension': c.office_phone_extension,
            'email': c.email, 'work_email': c.work_email,
        }
        client_data = {
            'first_name': client.first_name, 'middle_initial': client.middle_initial, 'last_name': client.last_name,
            'client_number': client.client_number, 'client_date': client.client_date
        }

        form_list = CHM.form_generator(3)

        form_list[0] = AddressForm(data=address_data)
        form_list[1] = ContactForm(data=contact_data)
        form_list[2] = ClientForm(data=client_data)
        # For debugging
        CHM.form_errors_printer(form_list)

        self.assertTrue(form_list[0].is_valid())
        self.assertTrue(form_list[1].is_valid())
        self.assertTrue(form_list[2].is_valid())

    def test_create_sales_prospect_residential(self):
        a = Address.objects.get(pk=1111)
        self.assertTrue(isinstance(a, Address), 'address != Address')
        c = Contact.objects.get(pk=2222)
        self.assertTrue(isinstance(c, Contact), 'contact != Contact')
        liberty_contact = EmployeeFactory()
        # Sales Prospect
        sp = Sales_Prospect.objects.create_sales_prospect(first_name='Ken', middle_initial='L',
                                                          last_name='Salesprospect',
                                                          sp_liberty_contact=liberty_contact,
                                                          sales_type='New', sales_probability='L',
                                                          initial_contact_date='2014-1-15', comments='new lead.',
                                                          sp_address=a, sp_contact=c)
        self.assertTrue(isinstance(sp, Sales_Prospect), 'salesprospect != SalesProspect')
        # Form work
        address_data = {'street': a.street, 'unit': a.unit, 'city': a.city, 'state': a.state,
                        'zip_code': a.zip_code,
        }
        contact_data = {
            'phone': c.phone, 'cell': c.cell, 'office_phone': c.office_phone,
            'office_phone_extension': c.office_phone_extension,
            'email': c.email, 'work_email': c.work_email,
        }
        sales_prospect_data = {
            'first_name': sp.first_name, 'middle_initial': sp.middle_initial, 'last_name': sp.last_name,
            'sp_liberty_contact': sp.sp_liberty_contact_id, 'sales_type': sp.sales_type,
            'sales_probability': sp.sales_probability, 'initial_contact_date': sp.initial_contact_date,
            'comments': sp.comments
        }
        # form work
        form_list = CHM.form_generator(3)

        form_list[0] = AddressForm(data=address_data)
        form_list[1] = ContactForm(data=contact_data)
        form_list[2] = SalesProspectForm(data=sales_prospect_data)
        # For debugging
        CHM.form_errors_printer(form_list)
        # Verify forms are valid
        self.assertTrue(form_list[0].is_valid())
        self.assertTrue(form_list[1].is_valid())
        self.assertTrue(form_list[2].is_valid())

#endregion

#region SalesProspectFactory Test




#endregion

#region SalesProspectTest




#endregion

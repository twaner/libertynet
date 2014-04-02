from django.test import TestCase
from Common.models import Address, Contact, Card, Billing
import Common.factories as f
from Common.helpermethods import *
from Common.forms import AddressForm, ContactForm, EmployeeContactForm, CallListContactForm, \
    BillingForm, CardForm, InstallerForm, CallListForm
from Site.models import Site

#region FORM TESTS


class CommonFormTest(TestCase):
    print('Starting %s...' % TestCase.__name__)

    def test_address_form(self):
        a = f.AddressFactory()
        self.assertTrue(isinstance(a, Address), "Is not address AddressFormTest")
        address_data = {'street': a.street, 'unit': a.unit, 'city': a.city, 'state': a.state,
                        'zip_code': a.zip_code, }
        form = AddressForm(data=address_data)
        form_assert_true_worker(self, form)

        if form.is_valid():
            created_address = create_address_helper(form)
            assert_true_worker(self, Address, created_address)

    def test_contact_form_employee(self):
        c = f.ContactEmployeeFactory()
        self.assertTrue(isinstance(c, Contact), "Is not Contact")
        contact_data = {
            'phone': c.phone, 'cell': c.cell, 'email': c.email, 'work_email': c.work_email,
            'office_phone': c.office_phone, 'office_phone_extension': c.office_phone_extension
        }
        form = EmployeeContactForm(data=contact_data)
        form_assert_true_worker(self, form)
        if form.is_valid():
            created_contact = create_employee_contact_helper(form)
            assert_true_worker(self, Contact, created_contact)

    def test_contact_form(self):
        c = f.ContactFactory()
        self.assertTrue(isinstance(c, Contact), 'ContactFactory not contact!')
        contact_data = {
            'phone': c.phone, 'phone_extension': c.phone_extension, 'cell': c.cell, 'email': c.email,
            'work_email': c.work_email, 'office_phone': c.office_phone,
            'office_phone_extension': c.office_phone_extension, 'website': c.website
        }
        form = ContactForm(data=contact_data)
        form_errors_printer(form)
        form_assert_true_worker(self, form)

        if form.is_valid():
            created_contact = create_contact_helper(form)
            assert_true_worker(self, Contact, created_contact)

        # Test clean method
        # extension with no phone
        contact_data['phone'] = ''
        form = ContactForm(data=contact_data)
        form_assert_false_worker(self, form)

        # office phone
        contact_data['phone'] = '9789991111'
        contact_data['office_phone'] = ''
        form = ContactForm(data=contact_data)
        form_assert_false_worker(self, form)

    def test_call_list_contact_form(self):
        c = f.ContactFactory()
        self.assertTrue(isinstance(c, Contact))

        contact_data = {
            'phone': c.phone, 'cell': c.cell, 'email': c.email, 'work_email': c.work_email,
            'office_phone': c.office_phone, 'office_phone_extension': c.office_phone_extension,
            'website': c.website
        }
        form = CallListContactForm(data=contact_data)
        form_assert_true_worker(self, form)

        if form.is_valid():
            created_calllist = create_calllist_contact_helper(form)
            assert_true_worker(self, Contact, created_calllist)

    def test_call_list_form(self):
        cl = f.Call_ListFactory()

        call_list_data = {}
        form = CallListForm(data=call_list_data)
        form_assert_false_worker(self, form)

        call_list_data = {
            'first_name': cl.first_name, 'middle_initial': cl.middle_initial,
            'last_name': cl.last_name, 'cl_contact': cl.cl_contact,
            'cl_order': cl.cl_order, 'cl_is_enabled': cl.cl_is_enabled,
            'cl_genre': cl.cl_genre.genre_id
        }
        form = CallListForm(data=call_list_data)
        form_assert_true_worker(self, form)

        if form.is_valid():
            calllist = create_call_list_helper(form, cl.cl_contact, Site())

    def test_billing_form(self):
        b = f.BillingFactory()
        billing_data = {}
        form = BillingForm(data=billing_data)
        form_assert_false_worker(self, form)
        billing_data = {
            'profile_name': b.profile_name, 'method': b.method
        }
        form = BillingForm(data=billing_data)
        form_assert_true_worker(self, form)

        if form.is_valid():
            billing = create_billing_helper(form, Address(), Card())
            assert_true_worker(self, Billing, billing)

    def test_card_form(self):
        c = f.CardFactory()
        card_data = {}
        form = CardForm(data=card_data)
        form_assert_false_worker(self, form)

        card_data = {
            'first_name': c.first_name, 'middle_initial': c.middle_initial,
            'last_name': c.last_name, 'card_number': c.card_number, 'card_code': c.card_code,
            'card_type': c.card_type, 'card_expiration': c.card_expiration
        }
        form = CardForm(data=card_data)
        form_assert_true_worker(self, form)

        if form.is_valid():
            card = create_card_helper(form)
            assert_true_worker(self, Card, card)

        # Test clean method
        card_data['card_expiration'] = '2013-1-12'
        form = CardForm(data=card_data)
        form_assert_false_worker(self, form)

    def test_installer_form(self):
        i = f.InstallerFactory()
        i_data = {}
        form = InstallerForm(data=i_data)
        form_assert_false_worker(self, form)

        i_data = {
            'installer_code': i.installer_code, 'installer_company_name': i.installer_company_name,
            'installer_notes': i.installer_notes
        }
        form = InstallerForm(data=i_data)
        form_assert_true_worker(self, form)

#endregion

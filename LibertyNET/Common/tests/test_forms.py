from django.test import TestCase
from Common.models import Address, Contact, Card, Billing
import Common.factories as f
from Common.forms import AddressForm, ContactForm, EmployeeContactForm

#region FORM TESTS


class AddressFormTest(TestCase):
    def test_address_form(self):
        print("AddressFormTest")
        a = f.AddressFactory()
        self.assertTrue(isinstance(a, Address), "Is not address AddressFormTest")
        address_data = {'street': a.street, 'unit': a.unit, 'city': a.city, 'state': a.state,
                        'zip_code': a.zip_code, }
        form = AddressForm(data=address_data)
        self.assertTrue(form.is_valid(), "AddressForm not valid.")

    def test_contact_form_employee(self):
        print('test_contact_form_employee: ')
        c = f.ContactEmployeeFactory()
        self.assertTrue(isinstance(c, Contact), "Is not Contact")
        contact_date = {
            'phone': c.phone, 'cell': c.cell, 'email': c.email, 'work_email': c.work_email,
            'office_phone': c.office_phone, 'office_phone_extension': c.office_phone_extension
        }
        form = EmployeeContactForm(data=contact_date)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_valid(), "EmployeeContactForm is not valid")

    def test_contact_form(self):
        print('test_contact_form...')
        c = f.ContactFactory()
        self.assertTrue(isinstance(c, Contact), 'ContactFactory not contact!')
        contact_date = {
            'phone': c.phone, 'cell': c.cell, 'email': c.email, 'work_email': c.work_email,
            'office_phone': c.office_phone, 'office_phone_extension': c.office_phone_extension,
            'website': c.website
        }
        form = ContactForm(data=contact_date)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.is_valid(), "ContactForm is not valid")

#endregion

from django.test import TestCase
from Common.models import Address, Contact, Card, Billing
import Common.factories as f
from Common.forms import AddressForm, EmployeeContactForm

#region Address Test


class AddressEmployeeTest(TestCase):
    def create_address_employee(self, street="44 Broadway", unit="4B", city="Kingston", state="NY", zip_code="12401"):
        return Address.objects.create(street=street, unit=unit, city=city, state=state, zip_code=zip_code)

    def test_address_creation(self):
        a = self.create_address_employee()
        self.assertEqual("44 Broadway", a.street, "Street is not correct.")
        self.assertEqual(Address, type(a), "Type is not address.")
        self.assertTrue(isinstance(a, Address))
        self.assertEqual(a.__str__(), '44 Broadway 4B Kingston NY 12401')

#endregion

#region Contact


class ContactTest(TestCase):
    def create_contact_full(self, phone="8453334444", phone_extension="2", cell="8456667777",
                            office_phone="9142221111", office_phone_extension="33", email="test@test.com",
                            work_email="work@work.com", website="www.test.com"):
        return Contact.objects.create(phone=phone, phone_extension=phone_extension, cell=cell,
                                      office_phone=office_phone, office_phone_extension=office_phone_extension,
                                      email=email, work_email=work_email, website=website)

    def test_create_contact_full_creation(self):
        c = self.create_contact_full()
        self.assertTrue(isinstance(c, Contact), "Is not Contact [full]")


class ContactEmployeeTest(TestCase):
    def create_contact_employee(self, phone="8453334444", cell="8456667777", office_phone='6549087711',
                                office_phone_extension='888', email="test@test.com", work_email="work@work.com"):
        return Contact.objects.create(phone=phone, cell=cell, email=email, work_email=work_email,
                                      office_phone=office_phone, office_phone_extension=office_phone_extension)

    def test_create_contact_employee(self):
        con = self.create_contact_employee()
        self.assertTrue(isinstance(con, Contact), "Employee Contact is not instance")

#endregion

#region Factory Tests


class FactoryTestCase(TestCase):
    def test_address_factory(self):
        address = f.AddressFactory()
        self.assertTrue(isinstance(address, Address), "AddressFactory is not address")

    def test_contact_employee_factory(self):
        contact = f.ContactEmployeeFactory()
        self.assertTrue(isinstance(contact, Contact),
                        "ContactEmployeeFactory is not Contact")

    def test_contact_factory(self):
        contact = f.ContactFactory()
        self.assertTrue(isinstance(contact, Contact), 'ContactFactory !Contact')

    def test_card_factory(self):
        card = f.CardFactory()
        self.assertTrue(isinstance(card, Card), "CardFactory is not Card")

    def test_billing_factory(self):
        billing = f.BillingFactory()
        self.assertTrue(isinstance(billing, Billing), "BillingFactory is not Billing")

#endregion
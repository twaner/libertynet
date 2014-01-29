from django.test import TestCase
from Common.models import Address, Contact, Card, Billing, Installer, Genre, Call_List
import Common.factories as f
from Common.forms import AddressForm, EmployeeContactForm

#region Globals


add = dict(street='44 Broadway', unit='4B', city='Kingston', state='NY', zip_code='12401')
con = dict(phone="8453334444", phone_extension="2", cell="8456667777",
           office_phone="9142221111", office_phone_extension="33", email="test@test.com",
           work_email="work@work.com", website="www.test.com")
econ = dict(phone="8453334444", cell="8456667777", office_phone='6549087711',
            office_phone_extension='888', email="test@test.com", work_email="work@work.com")
card = dict(first_name='Liam', middle_initial='L', last_name='Larson', card_number='5432123',
            card_code='555', card_type='VISA')

#endregion

#region Address Test


class AddressEmployeeTest(TestCase):
    print('Starting AddressEmployeeTest...')

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
    print('Starting ContactTest...')

    def create_contact_full(self, phone="8453334444", phone_extension="2", cell="8456667777",
                            office_phone="9142221111", office_phone_extension="33", email="test@test.com",
                            work_email="work@work.com", website="www.test.com"):
        return Contact.objects.create(phone=phone, phone_extension=phone_extension, cell=cell,
                                      office_phone=office_phone, office_phone_extension=office_phone_extension,
                                      email=email, work_email=work_email, website=website)

    def test_create_contact_full_creation(self):
        c = self.create_contact_full()
        self.assertTrue(isinstance(c, Contact), "Is not Contact [full]")
        self.assertEqual(c.__str__(), '845-333-4444', '__str__() does not match phone')
        self.assertEqual(c.phone_extension_helper(), '845-333-4444 ext. 2', 'extension helper not matching.')


class ContactEmployeeTest(TestCase):
    print('Starting ContactEmployeeTest...')

    def create_contact_employee(self, phone="8453334444", cell="8456667777", office_phone='6549087711',
                                office_phone_extension='888', email="test@test.com", work_email="work@work.com"):
        return Contact.objects.create(phone=phone, cell=cell, email=email, work_email=work_email,
                                      office_phone=office_phone, office_phone_extension=office_phone_extension)

    def test_create_contact_employee(self):
        con = self.create_contact_employee()
        self.assertTrue(isinstance(con, Contact), "Employee Contact is not instance")

#endregion

#region Billing Test

class CardTest(TestCase):
    def create_card(self, first_name='Liam', middle_initial='L', last_name='Larson', card_number='5432123',
                    card_code='555', card_type='VISA'):
        return Card.objects.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                                   card_number=card_number, card_code=card_code, card_type=card_type)

    def test_create_card(self):
        card = self.create_card()
        self.assertTrue(isinstance(card, Card), 'card is not Card')
        self.assertEqual(card.__str__(), 'Card Info: Liam Larson', '__str__ does not match')


class BillingTest(TestCase):
    """
    def create_billing(self, profile_name='Primary', method=454, billing_address=f.AddressFactory(),
                       card=f.CardFactory()):
        return Billing.objects.create(profile_name=profile_name, method=method, billing_address=billing_address,
                                      card=card)
    """

    def setUp(self):
        card = Card.objects.create(card_id=787, first_name='Kelly', middle_initial='K', last_name='Klark',
                                   card_number='123456', card_code='543', card_type='VISA')
        address = Address.objects.create(id=989, street="44 Broadway", unit="4B", city="Kingston", state="NY",
                                         zip_code="12401")

    def test_create_billing(self):
        card = Card.objects.get(pk=787)
        self.assertTrue(isinstance(card, Card), 'Did not setUP Card')
        address = Address.objects.get(pk=989)
        self.assertTrue(isinstance(address, Address), "Did nto setUp Address")
        billing = Billing.objects.create(profile_name='Primary', method=454, billing_address=address,
                                         card=card)

        self.assertTrue(isinstance(billing, Billing), 'billing != Billing')
        self.assertEqual(billing.__str__(), 'Primary', '__str__ not working')


#endregion

#region Factory Tests


class FactoryTestCase(TestCase):
    print('Starting FactoryTestCases...')

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

    def test_installer_factory(self):
        installer = f.InstallerFactory()
        self.assertTrue(isinstance(installer, Installer), 'InstallerFactory !Installer')

    def test_call_list_factory(self):
        call_list = f.Call_ListFactory()
        self.assertTrue(isinstance(call_list, Call_List), 'CallListFactory !Call_List')

    def test_genre_factory(self):
        genre = f.GenreFactory()
        self.assertTrue(isinstance(genre, Genre), 'GenreFactory !Genre')

        #endregion

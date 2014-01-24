import factory
import factory.fuzzy
from models import Address, Contact, Card, Billing, Installer, Genre, Call_List


class AddressFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Address
    id = factory.Sequence(lambda n: '999%d' % n)
    street = factory.Sequence(lambda n: '%02d Test St' % n)
    unit = factory.Sequence(lambda n: '%dB' % n)
    city = factory.fuzzy.FuzzyText(length=4, prefix='Testcity')
    state = 'New York'
    zip_code = factory.Sequence(lambda n: '%05d' % n)


class ContactEmployeeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact
    id = factory.Sequence(lambda n: '889%d' % n)
    phone = factory.Sequence(lambda n: '845678%04d' % n)
    #phone = '8769091212'
    cell = factory.Sequence(lambda n: '97811122%02d' % n)
    office_phone = factory.Sequence(lambda n: '97811144%02d' % n)
    office_phone_extension = factory.Sequence(lambda n: '34%d' % n)
    email = 'test@test.com'
    work_email = 'work.test@test.com'


class ContactFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact
    id = factory.Sequence(lambda n: '889%d' % n)
    phone = factory.Sequence(lambda n: '845444%04d' % n)
    phone_extension = factory.Sequence(lambda n: '%03d' % n)
    cell = factory.Sequence(lambda n: '97811122%02d' % n)
    office_phone = factory.Sequence(lambda n: '97811144%02d' % n)
    office_phone_extension = factory.Sequence(lambda n: '34%d' % n)
    email = 'contactfull@contactfull.com'
    work_email = 'work.contact@workcontact.com'
    website = 'www.contactwebsite.com'


class CardFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Card
    first_name = 'John'
    middle_initial = 'E'
    last_name = 'Cardtest'
    card_number = factory.Sequence(lambda n: '%08d' % n)
    card_code = factory.Sequence(lambda n: '%04d' % n)
    card_type = 'VISA'


class BillingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Billing
    profile_name = 'Johnson Billing'
    method = factory.Sequence(lambda n: '%04d' % n)
    billing_address = factory.SubFactory(AddressFactory)
    card = factory.SubFactory(CardFactory)


class InstallerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Installer
    installer_id = 9898
    installer_code = 7654
    installer_company_name = 'Liberty Security Services'
    installer_notes = "test note text."


class GenreFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Genre
    genre_id = 1
    genre = 'General Call List'
    genre_description = 'Non-specific call list.'


class Call_ListFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Call_List
    call_list_id = 4545
    cl_contact = factory.SubFactory(ContactFactory)
    cl_order = '2'
    cl_is_enabled = True
    cl_genre = factory.SubFactory(GenreFactory)


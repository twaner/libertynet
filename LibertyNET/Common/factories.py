import factory
import factory.fuzzy
from models import Address, Contact, Card, Billing


class AddressFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Address
    id = factory.sequence(lambda n: '999%d' % n)
    street = factory.sequence(lambda n: '%02d Test St' % n)
    unit = factory.sequence(lambda n: '%dB' % n)
    city = factory.fuzzy.FuzzyText(length=4, prefix='Testcity')
    state = 'New York'
    zip_code = factory.sequence(lambda n: '%05d' % n)


class ContactEmployeeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact
    id = factory.sequence(lambda n: '889%d' % n)
    phone = factory.sequence(lambda n: '84567809%02d' % n)
    cell = factory.sequence(lambda n: '97811122%02d' % n)
    office_phone = factory.sequence(lambda n: '97811144%02d' % n)
    office_phone_extension = factory.sequence(lambda n: '34%d' % n)
    email = 'test@test.com'
    work_email = 'work.test@test.com'


class ContactFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Contact
    id = factory.sequence(lambda n: '889%d' % n)
    phone = factory.sequence(lambda n: '84567809%02d' % n)
    phone_extension = factory.sequence(lambda n: '%03d' % n)
    cell = factory.sequence(lambda n: '97811122%02d' % n)
    office_phone = factory.sequence(lambda n: '97811144%02d' % n)
    office_phone_extension = factory.sequence(lambda n: '34%d' % n)
    email = 'contactfull@contactfull.com'
    work_email = 'work.contact@workcontact.com'


class CardFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Card
    first_name = 'John'
    middle_initial = 'E'
    last_name = 'Cardtest'
    card_number = factory.sequence(lambda n: '%12d' % n)
    card_code = factory.sequence(lambda n: '%04d' % n)
    card_type = 'VISA'


class BillingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Billing
    profile_name = 'Johnson Billing'
    method = factory.sequence(lambda n: '%04d' % n)
    billing_address = factory.SubFactory(AddressFactory)
    card = factory.SubFactory(CardFactory)




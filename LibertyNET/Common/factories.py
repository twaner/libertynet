import factory
from models import Address, Contact


class AddressFactory(factory.Factory):
    FACTORY_FOR = Address
    id = factory.sequence(lambda n: '999%d' % n)
    street = '44 Test St'
    unit = '4B'
    city = 'Kingston'
    state = 'New York'
    zip_code = '12401'


class ContactEmployeeFactory(factory.Factory):
    FACTORY_FOR = Contact
    id = factory.sequence(lambda n: '889%d' % n)
    phone = '8456780987'
    cell = '9781112222'
    email = 'test@test.com'
    work_email = 'work.test@test.com'
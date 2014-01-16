import factory
from models import Address, Contact


class AddressFactory(factory.Factory):
    FACTORY_FOR = Address
    id = 1
    street = '44 Test St'
    unit = '4B'
    city = 'Kingston'
    state = 'NY'
    zip_code = '12401'


class ContactEmployeeFactory(factory.Factory):
    FACTORY_FOR = Contact
    id = 1
    phone = '8456780987'
    cell = '9781112222'
    email = 'test@test.com'
    work_email = 'work.test@test.com'
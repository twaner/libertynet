import factory
import factory.fuzzy
from models import Client, Sales_Prospect
from Common.factories import *

#region Client Factories


class ClientFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Client
    client_id = 967
    first_name = 'Stephen'
    middle_initial = 'Q'
    last_name = 'Clienttest'
    client_number = 8989
    business_name = None
    is_business = False
    client_address = factory.SubFactory(AddressFactory)
    client_contact = factory.SubFactory(ContactFactory)
    client_billing = factory.SubFactory(BillingFactory)
    client_date = '2014-01-13'


class ClientFactoryNoBilling(factory.DjangoModelFactory):
    FACTORY_FOR = Client
    client_id = 967
    first_name = 'Stephen'
    middle_initial = 'Q'
    last_name = 'Clienttest'
    client_number = 8989
    business_name = None
    is_business = False
    client_address = factory.SubFactory(AddressFactory)
    client_contact = factory.SubFactory(ContactFactory)
    client_date = '2014-01-13'


#endregion

#region SalesProspect Factories


class SalesProspect(factory.DjangoModelFactory):
    FACTORY_FOR = Sales_Prospect

#endregion
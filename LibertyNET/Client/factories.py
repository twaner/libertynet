import factory
import factory.fuzzy
from models import Client, SalesProspect
from Common.factories import *
from Employee.factories import *

#region Client Factories


class ClientFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Client
    client_id = factory.fuzzy.FuzzyInteger(99, 200)
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
    client_id = 977
    first_name = 'Stephen'
    middle_initial = 'Q'
    last_name = 'Clienttest'
    client_number = 8989
    business_name = None
    is_business = False
    client_address = factory.SubFactory(AddressFactory)
    client_contact = factory.SubFactory(ContactFactory)
    client_date = '2014-01-13'


class ClientFactoryBusiness(factory.DjangoModelFactory):
    FACTORY_FOR = Client
    client_id = 987
    first_name = 'Stephen'
    middle_initial = 'Q'
    last_name = 'Clienttest'
    client_number = 4432
    business_name = 'Clientbusiness'
    is_business = True
    client_address = factory.SubFactory(AddressFactory)
    client_contact = factory.SubFactory(ContactFactory)
    client_date = '2014-01-19'


#endregion

#region SalesProspect Factories


class SalesProspectResidentialFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SalesProspect
    sales_prospect_id = 999
    first_name = 'Sally'
    middle_initial = 'P'
    last_name = 'Salesprospect'
    sp_liberty_contact = factory.SubFactory(EmployeeFactory)
    sales_type = "Takeover"
    sales_probability = 'M'
    initial_contact_date = '2014-01-21'
    comments = 'Met at local function.'
    sp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory.create())
    sp_contact = factory.lazy_attribute(lambda a: Common.factories.ContactEmployeeFactory.create())


class SalesProspectBusinessFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SalesProspect
    sales_prospect_id = 9901
    first_name = 'John'
    middle_initial = 'P'
    last_name = 'Businessprospect'
    sp_business_name = 'Salesprospectbusiness'
    is_business = True
    sp_liberty_contact = factory.SubFactory(EmployeeFactory)
    sales_type = "New Account"
    sales_probability = 'M'
    initial_contact_date = '2014-01-11'
    comments = 'Met at local dinner.'
    sp_address = factory.SubFactory(AddressFactory)
    sp_contact = factory.SubFactory(ContactFactory)

#endregion
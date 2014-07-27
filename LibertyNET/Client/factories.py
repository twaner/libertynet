import factory
import factory.fuzzy
from models import Client, ClientCallLog, SalesProspect, SalesProspectCallLog
from Common.factories import *
from Employee.factories import *
from Common.helpermethods import date_change


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
    client_id = factory.Sequence(lambda n: '89%d' % n)
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
    id = factory.Sequence(lambda n: '81%d' % n)
    first_name = 'Sally'
    middle_initial = 'P'
    last_name = 'Salesprospect'
    sp_liberty_contact = factory.SubFactory(EmployeeFactory)
    sales_type = "Takeover"
    sales_probability = 'M'
    initial_contact_date = '2014-01-21'
    comments = 'Met at local function.'
    service_guide = False
    sp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory.create())
    sp_contact = factory.lazy_attribute(lambda a: Common.factories.ContactEmployeeFactory.create())


class SalesProspectBusinessFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SalesProspect
    id = factory.Sequence(lambda n: '89%d' % n)
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
    service_guide = False
    sp_address = factory.SubFactory(AddressFactory)
    sp_contact = factory.SubFactory(ContactFactory)


#endregion

#region CallListFactories


class ClientCallLogFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ClientCallLog
    id = factory.fuzzy.FuzzyInteger(19, 50)
    client_id = factory.SubFactory(ClientFactoryBusiness)
    caller = factory.SubFactory(EmployeeDjangoFactory)
    call_date = date_change(-4)
    call_time = '13:13'
    purpose = 'ClientCallLog purpose'
    notes = 'ClientCallLog notes'
    next_contact = date_change(20)
    follow_up = False


class SalesProspectCallLogFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SalesProspectCallLog
    id = factory.fuzzy.FuzzyInteger(19, 50)
    sales_id = factory.SubFactory(SalesProspectResidentialFactory)
    caller = factory.SubFactory(EmployeeFactory)
    call_date = date_change(-4)
    call_time = '13:13'
    purpose = 'ClientCallLog purpose'
    notes = 'ClientCallLog notes'
    next_contact = date_change(20)
    follow_up = False


class ClientCallLogFollowFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ClientCallLog
    id = factory.fuzzy.FuzzyInteger(19, 50)
    client_id = factory.SubFactory(ClientFactoryBusiness)
    caller = factory.SubFactory(EmployeeDjangoFactory)
    call_date = date_change(-4)
    call_time = '13:13'
    purpose = 'ClientCallLog purpose'
    notes = 'ClientCallLog notes'
    next_contact = date_change(20)
    follow_up = True


class SalesProspectCallLogFollowFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SalesProspectCallLog
    id = factory.fuzzy.FuzzyInteger(19, 50)
    sales_id = factory.SubFactory(SalesProspectResidentialFactory)
    caller = factory.SubFactory(EmployeeFactory)
    call_date = date_change(-4)
    call_time = '13:13'
    purpose = 'ClientCallLog purpose'
    notes = 'ClientCallLog notes'
    next_contact = date_change(20)
    follow_up = True
#endregion
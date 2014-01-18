import factory
import factory.fuzzy
from models import Client, Sales_Prospect

#region Client Factories


class ClientFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Client


#endregion

#region SalesProspect Factories


class SalesProspect(factory.DjangoModelFactory):
    FACTORY_FOR = Sales_Prospect

#endregion
from django.test import TestCase
from Common.models import Address, Contact, Card, Billing
from Common.factories import *
from models import Client, Sales_Prospect
from factories import *

#region ClientFactoryTest


class FactoryTests(TestCase):
    def test_create_client_factory(self):
        print('Starting test_create_client_factory...')
        client = ClientFactory()
        self.assertTrue(isinstance(client, Client), "ClientFactory - !Client")
        self.assertTrue(isinstance(client.client_billing, Billing), "ClientFactory - !client_billing")

    def test_create_client_factory_no_billing(self):
        print('Starting test_create_client_factory_no_billing...')
        client = ClientFactoryNoBilling
        self.assertTrue(isinstance(client, Client), 'ClientFactoryNoBilling !Client')

#endregion

#region ClientTest




#endregion

#region SalesProspectFactory Test




#endregion

#region SalesProspectTest




#endregion

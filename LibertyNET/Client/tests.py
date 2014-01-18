from django.test import TestCase
from Common.models import Address, Contact, Card, Billing
from Common.factories import *
from models import Client, Sales_Prospect
from factories import *

#region ClientFactory


class FactoryTests(TestCase):
    def test_create_client(self):
        client = ClientFactory()
        self.assertTrue(isinstance(client, Client), "ClientFactory is not Client")
        self.assertTrue(isinstance(client.client_billing, Billing), "!client_billing")

#endregion

#region ClientTest




#endregion



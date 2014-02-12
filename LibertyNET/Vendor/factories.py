import factory
import factory.fuzzy
from Vendor.models import Manufacturer, Supplier, SupplierList
import Common.factories as cf

#region Factories


class SupplierFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Supplier
    supplier_id = factory.Sequence(lambda n: '%04d' % n, type=int)
    supplier_company_id = 6543
    supplier_contact_id = factory.SubFactory(cf.ContactFactory)
    account_id = 8712

class SupplierListFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SupplierList
    supplier_list_id = 9010
    supplier_id = factory.SubFactory(SupplierFactory)
    position_id = '2'


class ManufacturerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Manufacturer
    manufacturer_id = factory.Sequence(lambda n: '%04d' % n, type=int)  #1928
    name = 'Manfacturer name'
    manu_address = factory.SubFactory(cf.AddressFactory)
    manu_contact = factory.SubFactory(cf.ContactFactory)
    manu_primary_supplier = factory.SubFactory(SupplierFactory)
    manu_secondary_supplier = factory.SubFactory(SupplierFactory)
    is_direct = True

#endregion
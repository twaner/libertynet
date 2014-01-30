from django.test import TestCase
from Vendor.factories import ManufacturerFactory, SupplierFactory, SupplierListFactory
from Vendor.models import Manufacturer, Supplier, Supplier_List

#region Vendor Test


class FactoryTestCases(TestCase):
    print('Starting FactoryTestCases Vendor...')

    def test_manufacturer_factory(self):
        manufacturer = ManufacturerFactory()
        self.assertTrue(isinstance(manufacturer, Manufacturer),
                        'ManufacturerFactory is not Manufacturer')

    def test_supplier_factory(self):
        supplier = SupplierFactory()
        print('supplier.supplier_id', supplier.supplier_id)
        self.assertTrue(isinstance(supplier, Supplier), 'SupplierFactory is not Supplier')

    def test_supplier_list_factory(self):
        supplier_list = SupplierListFactory()
        self.assertTrue(isinstance(supplier_list, Supplier_List), 'SupplierListFactory is not SupplierList')

#endregion

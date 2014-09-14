__author__ = 'taiowawaner'
from Vendor.models import Supplier, SupplierList, Manufacturer


#region Supplier

def create_supplier_helper(form, contact):
    company = form.cleaned_data['supplier_company']
    contact = contact
    account = form.cleaned_data['account']

    supplier = Supplier.object.create_supplier_list(company, contact, account)
    return supplier

# end region

#region Manufacturer


def create_manufacturer_helper(form, address, contact):
    name = form.cleaned_data['name']
    primary_supplier = form.cleaned_data['primary_supplier']
    secondary_supplier = form.cleaned_data['secondary_supplier']

    manufacturer = Manufacturer.object.create_manufacturer(name, address, contact,
                                                           primary_supplier, secondary_supplier)
    return manufacturer


#end region
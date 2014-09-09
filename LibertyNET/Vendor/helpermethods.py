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

from django.db import models
from Common.models import NUMBER_CHOICES

#region Models

class Manufacturer(models.Model):
    #TODO ==> Should this be a business with a human contact?
    manufacturer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    manu_address = models.ForeignKey('Common.Address', blank=True, null=True)
    manu_contact = models.ForeignKey('Common.Contact', blank=True, null=True)
    manu_primary_supplier = models.ForeignKey('Vendor.Supplier', related_name="primary supplier",blank=True, null=True)
    manu_secondary_supplier = models.ForeignKey('Vendor.Supplier', related_name="secondary supplier",blank=True, null=True)
    #TODO ==> What is default?
    is_direct = models.BooleanField(default=False)

    #TODO ==> _unicode_

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    #TODO ==> How do we handle this
    supplier_company_id = models.IntegerField(max_length=11)
    supplier_contact_id = models.IntegerField(max_length=11)
    account_id = models.IntegerField(max_length=11)

    #TODO ==> _unicode_

class Supplier_List(models.Model):
    supplier_list_id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey('Vendor.Supplier')
    position_id = models.IntegerField(choices=NUMBER_CHOICES)

#endregion
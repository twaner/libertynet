from django.db import models
from django.utils.encoding import force_bytes
from Common.models import NUMBER_CHOICES

#region ModelManagers


class ManufacturerManager(models.Manager):
    def create_manufacturer(self, name, manu_address, manu_contact, manu_primary_supplier,
                            manu_secondary_supplier, is_direct):
        """
        Creates a manufacturer.
        @rtype : Manufacturer
        @param name: name.
        @param manu_address: Address.
        @param manu_contact: Contact.
        @param manu_primary_supplier: Primary Supplier.
        @param manu_secondary_supplier: Secondary Supplier.
        @param is_direct:
        @return:
        """
        manufacturer = self.create(name=name, manu_address=manu_address,
                                   manu_contact=manu_contact, manu_primary_supplier=manu_primary_supplier,
                                   manu_secondary_supplier=manu_secondary_supplier, is_direct=is_direct)
        manufacturer.save()
        return manufacturer


class SupplierManager(models.Manager):
    def create_supplier(self, supplier_company_id, supplier_contact_id, account_id):
        supplier = self.create(supplier_company_id=supplier_company_id,
                               supplier_contact_id=supplier_contact_id, account_id=account_id)
        supplier.save()
        return supplier


class SupplierListManager(models.Manager):
    def create_supplier_list(self, supplier_id, position_id):
        supplier_list = self.create(supplier_id=supplier_id, position_id=position_id)
        supplier_list.save()
        return supplier_list

#endregion

#region Models


class Manufacturer(models.Model):
    #TODO ==> Should this be a business with a human contact?
    manufacturer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    manu_address = models.ForeignKey('Common.Address', blank=True, null=True)
    manu_contact = models.ForeignKey('Common.Contact', blank=True, null=True)
    manu_primary_supplier = models.ForeignKey('Vendor.Supplier', related_name="primary supplier", blank=True, null=True)
    manu_secondary_supplier = models.ForeignKey('Vendor.Supplier', related_name="secondary supplier", blank=True,
                                                null=True)
    #TODO ==> What is default?
    is_direct = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.name


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    #TODO ==> How do we handle this make a FK
    #TODO ==> Supplier name?
    supplier_company_id = models.IntegerField(max_length=11)
    #supplier_contact_id = models.IntegerField(max_length=11)
    supplier_contact_id = models.ForeignKey('Common.Contact')
    account_id = models.IntegerField(max_length=11)

    def __str__(self):
        return force_bytes('%s' % self.account_id)


class SupplierList(models.Model):
    supplier_list_id = models.AutoField(primary_key=True)
    supplier_id = models.ForeignKey('Vendor.Supplier')
    position_id = models.IntegerField(choices=NUMBER_CHOICES)

    #TODO ==> def __str__(self):

#endregion
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Manufacturer'
        db.create_table(u'Vendor_manufacturer', (
            ('manufacturer_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'], null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Contact'], null=True, blank=True)),
            ('primary_supplier', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='primary supplier', null=True, to=orm['Vendor.Supplier'])),
            ('secondary_supplier', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secondary supplier', null=True, to=orm['Vendor.Supplier'])),
            ('is_direct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Vendor', ['Manufacturer'])

        # Adding model 'Supplier'
        db.create_table(u'Vendor_supplier', (
            ('supplier_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier_company_id', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('supplier_contact_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Contact'])),
            ('account', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
        ))
        db.send_create_signal(u'Vendor', ['Supplier'])

        # Adding model 'SupplierList'
        db.create_table(u'Vendor_supplierlist', (
            ('supplier_list_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Vendor.Supplier'])),
            ('position_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Vendor', ['SupplierList'])


    def backwards(self, orm):
        # Deleting model 'Manufacturer'
        db.delete_table(u'Vendor_manufacturer')

        # Deleting model 'Supplier'
        db.delete_table(u'Vendor_supplier')

        # Deleting model 'SupplierList'
        db.delete_table(u'Vendor_supplierlist')


    models = {
        u'Common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NY'", 'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Common.contact': {
            'Meta': {'object_name': 'Contact'},
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office_phone': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'office_phone_extension': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'phone_extension': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'work_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'})
        },
        u'Vendor.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'is_direct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']", 'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']", 'null': 'True', 'blank': 'True'}),
            'primary_supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary supplier'", 'null': 'True', 'to': u"orm['Vendor.Supplier']"}),
            'secondary_supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary supplier'", 'null': 'True', 'to': u"orm['Vendor.Supplier']"}),
            'manufacturer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Vendor.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'account': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'supplier_company_id': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'supplier_contact_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'supplier_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Vendor.supplierlist': {
            'Meta': {'object_name': 'SupplierList'},
            'position_id': ('django.db.models.fields.IntegerField', [], {}),
            'supplier_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Vendor.Supplier']"}),
            'supplier_list_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Vendor']
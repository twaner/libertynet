# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'Client_client', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('middle_initial', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_number', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('business_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('is_business', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('client_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
            ('client_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Contact'])),
            ('client_billing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Billing'], null=True, blank=True)),
            ('client_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'Client', ['Client'])

        # Adding model 'SalesProspect'
        db.create_table(u'Client_salesprospect', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('middle_initial', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sp_business_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('is_business', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sp_liberty_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'], null=True, blank=True)),
            ('sales_type', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('sales_probability', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('initial_contact_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('sp_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'], null=True, blank=True)),
            ('sp_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Contact'], null=True, blank=True)),
            ('is_client', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('service_guide', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Client', ['SalesProspect'])

        # Adding model 'ClientCallLog'
        db.create_table(u'Client_clientcalllog', (
            ('caller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'], null=True, blank=True)),
            ('call_date', self.gf('django.db.models.fields.DateField')()),
            ('call_time', self.gf('django.db.models.fields.TimeField')()),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('next_contact', self.gf('django.db.models.fields.DateField')()),
            ('follow_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.Client'])),
        ))
        db.send_create_signal(u'Client', ['ClientCallLog'])

        # Adding model 'SalesProspectCallLog'
        db.create_table(u'Client_salesprospectcalllog', (
            ('caller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'], null=True, blank=True)),
            ('call_date', self.gf('django.db.models.fields.DateField')()),
            ('call_time', self.gf('django.db.models.fields.TimeField')()),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('next_contact', self.gf('django.db.models.fields.DateField')()),
            ('follow_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sales_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.SalesProspect'])),
        ))
        db.send_create_signal(u'Client', ['SalesProspectCallLog'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'Client_client')

        # Deleting model 'SalesProspect'
        db.delete_table(u'Client_salesprospect')

        # Deleting model 'ClientCallLog'
        db.delete_table(u'Client_clientcalllog')

        # Deleting model 'SalesProspectCallLog'
        db.delete_table(u'Client_salesprospectcalllog')


    models = {
        u'Client.client': {
            'Meta': {'object_name': 'Client'},
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'client_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'client_billing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Billing']", 'null': 'True', 'blank': 'True'}),
            'client_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'client_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'client_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'is_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_initial': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'Client.clientcalllog': {
            'Meta': {'object_name': 'ClientCallLog'},
            'call_date': ('django.db.models.fields.DateField', [], {}),
            'call_time': ('django.db.models.fields.TimeField', [], {}),
            'caller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Employee.Employee']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.Client']"}),
            'follow_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_contact': ('django.db.models.fields.DateField', [], {}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'Client.salesprospect': {
            'Meta': {'object_name': 'SalesProspect'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_contact_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_client': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_initial': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'sales_probability': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sales_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'service_guide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sp_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']", 'null': 'True', 'blank': 'True'}),
            'sp_business_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sp_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']", 'null': 'True', 'blank': 'True'}),
            'sp_liberty_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Employee.Employee']", 'null': 'True', 'blank': 'True'})
        },
        u'Client.salesprospectcalllog': {
            'Meta': {'object_name': 'SalesProspectCallLog'},
            'call_date': ('django.db.models.fields.DateField', [], {}),
            'call_time': ('django.db.models.fields.TimeField', [], {}),
            'caller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Employee.Employee']", 'null': 'True', 'blank': 'True'}),
            'follow_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_contact': ('django.db.models.fields.DateField', [], {}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'sales_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.SalesProspect']"})
        },
        u'Common.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NY'", 'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Common.billing': {
            'Meta': {'object_name': 'Billing'},
            'billing_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']", 'null': 'True', 'blank': 'True'}),
            'card': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Card']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'profile_name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Common.card': {
            'Meta': {'object_name': 'Card'},
            'card_code': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'card_expiration': ('django.db.models.fields.DateField', [], {}),
            'card_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'card_number': ('django.db.models.fields.IntegerField', [], {'max_length': '20'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_initial': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
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
        u'Employee.employee': {
            'Meta': {'object_name': 'Employee'},
            'emp_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'emp_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'emp_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'emp_title': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Employee.Title']", 'symmetrical': 'False'}),
            'employee_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hire_date': ('django.db.models.fields.DateField', [], {}),
            'is_terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_initial': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'pay_type': ('django.db.models.fields.CharField', [], {'default': "'HR'", 'max_length': '12'}),
            'termination_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'termination_reason': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'Employee.title': {
            'Meta': {'object_name': 'Title'},
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Client']
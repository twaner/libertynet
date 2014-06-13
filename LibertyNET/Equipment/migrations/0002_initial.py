# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'Equipment_device', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('device_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_system_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.System'], null=True, blank=True)),
            ('device_location', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('device_function', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('device_zone_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.Zone'], null=True, blank=True)),
        ))
        db.send_create_signal(u'Equipment', ['Device'])

        # Adding M2M table for field device_part_id on 'Device'
        m2m_table_name = db.shorten_name(u'Equipment_device_device_part_id')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('device', models.ForeignKey(orm[u'Equipment.device'], null=False)),
            ('part', models.ForeignKey(orm[u'Equipment.part'], null=False))
        ))
        db.create_unique(m2m_table_name, ['device_id', 'part_id'])

        # Adding M2M table for field camera_id on 'Device'
        m2m_table_name = db.shorten_name(u'Equipment_device_camera_id')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('device', models.ForeignKey(orm[u'Equipment.device'], null=False)),
            ('camera', models.ForeignKey(orm[u'Equipment.camera'], null=False))
        ))
        db.create_unique(m2m_table_name, ['device_id', 'camera_id'])

        # Adding model 'Panel'
        db.create_table(u'Equipment_panel', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('panel_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('panel_manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Vendor.Manufacturer'])),
            ('user_manual', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('installation_manual', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'Equipment', ['Panel'])

        # Adding model 'PartCategory'
        db.create_table(u'Equipment_partcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Equipment', ['PartCategory'])

        # Adding model 'Part'
        db.create_table(u'Equipment_part', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('part_manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Vendor.Manufacturer'])),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('flat_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Notes'], blank=True)),
            ('spec_sheet', self.gf('django.db.models.fields.TextField')()),
            ('install_guide', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.PartCategory'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_recalled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'Equipment', ['Part'])

        # Adding model 'Camera'
        db.create_table(u'Equipment_camera', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('camera_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('camera_system_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.System'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_wireless', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Equipment', ['Camera'])

        # Adding model 'ClientEstimate'
        db.create_table(u'Equipment_clientestimate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_name', self.gf('django.db.models.fields.TextField')(max_length=45)),
            ('estimate_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('preparer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('is_capital_improvement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_flat_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('sales_commission', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('prevailing_wage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('margin', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2, blank=True)),
            ('margin_guidelines', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('estimate_client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.Client'])),
        ))
        db.send_create_signal(u'Equipment', ['ClientEstimate'])

        # Adding M2M table for field estimate_parts on 'ClientEstimate'
        m2m_table_name = db.shorten_name(u'Equipment_clientestimate_estimate_parts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clientestimate', models.ForeignKey(orm[u'Equipment.clientestimate'], null=False)),
            ('estimate_parts_client', models.ForeignKey(orm[u'Equipment.estimate_parts_client'], null=False))
        ))
        db.create_unique(m2m_table_name, ['clientestimate_id', 'estimate_parts_client_id'])

        # Adding model 'SalesEstimate'
        db.create_table(u'Equipment_salesestimate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_name', self.gf('django.db.models.fields.TextField')(max_length=45)),
            ('estimate_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('preparer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('is_capital_improvement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_flat_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('sales_commission', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('prevailing_wage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('margin', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2, blank=True)),
            ('margin_guidelines', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('estimate_sales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.SalesProspect'])),
        ))
        db.send_create_signal(u'Equipment', ['SalesEstimate'])

        # Adding M2M table for field estimate_parts on 'SalesEstimate'
        m2m_table_name = db.shorten_name(u'Equipment_salesestimate_estimate_parts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('salesestimate', models.ForeignKey(orm[u'Equipment.salesestimate'], null=False)),
            ('estimate_parts_sales', models.ForeignKey(orm[u'Equipment.estimate_parts_sales'], null=False))
        ))
        db.create_unique(m2m_table_name, ['salesestimate_id', 'estimate_parts_sales_id'])

        # Adding model 'Estimate_Parts_Client'
        db.create_table(u'Equipment_estimate_parts_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estimate_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.ClientEstimate'])),
            ('part_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.Part'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('final_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('sub_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('flat_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('total_labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'Equipment', ['Estimate_Parts_Client'])

        # Adding model 'Estimate_Parts_Sales'
        db.create_table(u'Equipment_estimate_parts_sales', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estimate_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.SalesEstimate'])),
            ('part_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.Part'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('final_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('sub_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('flat_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('total_labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal(u'Equipment', ['Estimate_Parts_Sales'])


    def backwards(self, orm):
        # Deleting model 'Device'
        db.delete_table(u'Equipment_device')

        # Removing M2M table for field device_part_id on 'Device'
        db.delete_table(db.shorten_name(u'Equipment_device_device_part_id'))

        # Removing M2M table for field camera_id on 'Device'
        db.delete_table(db.shorten_name(u'Equipment_device_camera_id'))

        # Deleting model 'Panel'
        db.delete_table(u'Equipment_panel')

        # Deleting model 'PartCategory'
        db.delete_table(u'Equipment_partcategory')

        # Deleting model 'Part'
        db.delete_table(u'Equipment_part')

        # Deleting model 'Camera'
        db.delete_table(u'Equipment_camera')

        # Deleting model 'ClientEstimate'
        db.delete_table(u'Equipment_clientestimate')

        # Removing M2M table for field estimate_parts on 'ClientEstimate'
        db.delete_table(db.shorten_name(u'Equipment_clientestimate_estimate_parts'))

        # Deleting model 'SalesEstimate'
        db.delete_table(u'Equipment_salesestimate')

        # Removing M2M table for field estimate_parts on 'SalesEstimate'
        db.delete_table(db.shorten_name(u'Equipment_salesestimate_estimate_parts'))

        # Deleting model 'Estimate_Parts_Client'
        db.delete_table(u'Equipment_estimate_parts_client')

        # Deleting model 'Estimate_Parts_Sales'
        db.delete_table(u'Equipment_estimate_parts_sales')


    models = {
        u'Client.client': {
            'Meta': {'object_name': 'Client'},
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'client_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'client_billing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Billing']", 'null': 'True', 'blank': 'True'}),
            'client_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'client_date': ('django.db.models.fields.DateField', [], {}),
            'client_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'client_number': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'is_business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_initial': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
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
        u'Common.calllist': {
            'Meta': {'object_name': 'CallList'},
            'call_list_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'cl_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'cl_genre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Genre']"}),
            'cl_is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cl_order': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'middle_initial': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
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
        u'Common.genre': {
            'Meta': {'object_name': 'Genre'},
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'genre_description': ('django.db.models.fields.CharField', [], {'max_length': '144'}),
            'genre_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Common.installer': {
            'Meta': {'object_name': 'Installer'},
            'installer_code': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'installer_company_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'installer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installer_notes': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'Common.notes': {
            'Meta': {'object_name': 'Notes'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'purpose': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.TimeField', [], {})
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
        },
        u'Equipment.camera': {
            'Meta': {'object_name': 'Camera'},
            'camera_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'camera_system_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.System']"}),
            'is_wireless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'Equipment.clientestimate': {
            'Meta': {'object_name': 'ClientEstimate'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'estimate_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'estimate_client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.Client']"}),
            'estimate_parts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Equipment.Estimate_Parts_Client']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_capital_improvement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_name': ('django.db.models.fields.TextField', [], {'max_length': '45'}),
            'labor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'listed_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'listed_profit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'margin': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'margin_guidelines': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'preparer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Employee.Employee']"}),
            'prevailing_wage': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'sales_commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_flat_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_profit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'Equipment.device': {
            'Meta': {'object_name': 'Device'},
            'camera_id': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Equipment.Camera']", 'null': 'True', 'blank': 'True'}),
            'device_function': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'device_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'device_location': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'device_part_id': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Equipment.Part']", 'symmetrical': 'False'}),
            'device_system_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.System']", 'null': 'True', 'blank': 'True'}),
            'device_zone_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.Zone']", 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'Equipment.estimate_parts_client': {
            'Meta': {'object_name': 'Estimate_Parts_Client'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'estimate_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Equipment.ClientEstimate']"}),
            'final_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'flat_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Equipment.Part']"}),
            'profit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'sub_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'total_labor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'Equipment.estimate_parts_sales': {
            'Meta': {'object_name': 'Estimate_Parts_Sales'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'estimate_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Equipment.SalesEstimate']"}),
            'final_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'flat_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Equipment.Part']"}),
            'profit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'sub_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'total_labor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'Equipment.panel': {
            'Meta': {'object_name': 'Panel'},
            'installation_manual': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'panel_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel_manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Vendor.Manufacturer']"}),
            'user_manual': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Equipment.part': {
            'Meta': {'object_name': 'Part'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Equipment.PartCategory']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'flat_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'install_guide': ('django.db.models.fields.TextField', [], {}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_recalled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'labor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Notes']", 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'part_manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Vendor.Manufacturer']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'spec_sheet': ('django.db.models.fields.TextField', [], {})
        },
        u'Equipment.partcategory': {
            'Meta': {'object_name': 'PartCategory'},
            'category': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Equipment.salesestimate': {
            'Meta': {'object_name': 'SalesEstimate'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'estimate_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'estimate_parts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Equipment.Estimate_Parts_Sales']", 'symmetrical': 'False'}),
            'estimate_sales': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.SalesProspect']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_capital_improvement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_name': ('django.db.models.fields.TextField', [], {'max_length': '45'}),
            'labor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'listed_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'listed_profit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'margin': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'margin_guidelines': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'preparer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Employee.Employee']"}),
            'prevailing_wage': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'sales_commission': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_flat_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'total_profit': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'Site.network': {
            'Meta': {'object_name': 'Network'},
            'network_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'router_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'router_password': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'router_user_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'wifi_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'wifi_notes': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'wifi_password': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Site.site': {
            'Meta': {'object_name': 'Site'},
            'site_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'site_call_list': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Common.CallList']", 'null': 'True', 'blank': 'True'}),
            'site_client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.Client']"}),
            'site_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Site.system': {
            'Meta': {'object_name': 'System'},
            'backup_communications': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'is_system_local': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lockout_code': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'master_code': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'network_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.Network']"}),
            'panel_location': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'port': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'primary_communications': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'primary_power_location': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'secondary_communications': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'system_client_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.Client']"}),
            'system_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system_installer_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Installer']", 'null': 'True', 'blank': 'True'}),
            'system_ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'system_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'system_panel_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Equipment.Panel']", 'null': 'True', 'blank': 'True'}),
            'system_site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.Site']"}),
            'system_type_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Genre']"}),
            'tampered_id': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Site.zone': {
            'Meta': {'object_name': 'Zone'},
            'is_wireless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'system_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.System']"}),
            'zone_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_location': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'zone_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'zone_notes': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'Vendor.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'is_direct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'manu_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']", 'null': 'True', 'blank': 'True'}),
            'manu_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']", 'null': 'True', 'blank': 'True'}),
            'manu_primary_supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary supplier'", 'null': 'True', 'to': u"orm['Vendor.Supplier']"}),
            'manu_secondary_supplier': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary supplier'", 'null': 'True', 'to': u"orm['Vendor.Supplier']"}),
            'manufacturer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Vendor.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'account_id': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'supplier_company_id': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'supplier_contact_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'supplier_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Equipment']
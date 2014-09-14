# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ClientEstimate'
        db.delete_table(u'Equipment_clientestimate')

        # Removing M2M table for field estimate_parts on 'ClientEstimate'
        db.delete_table(db.shorten_name(u'Equipment_clientestimate_estimate_parts'))

        # Deleting model 'Estimate_Parts_Sales'
        db.delete_table(u'Equipment_estimate_parts_sales')

        # Deleting model 'Estimate_Parts_Client'
        db.delete_table(u'Equipment_estimate_parts_client')

        # Deleting model 'SalesEstimate'
        db.delete_table(u'Equipment_salesestimate')

        # Removing M2M table for field estimate_parts on 'SalesEstimate'
        db.delete_table(db.shorten_name(u'Equipment_salesestimate_estimate_parts'))

        # Adding field 'Part.quantity'
        db.add_column(u'Equipment_part', 'quantity',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=6, blank=True),
                      keep_default=False)


        # Renaming column for 'Part.notes' to match new field type.
        db.rename_column(u'Equipment_part', 'notes_id', 'notes')
        # Changing field 'Part.notes'
        db.alter_column(u'Equipment_part', 'notes', self.gf('django.db.models.fields.TextField')(max_length=300))
        # Removing index on 'Part', fields ['notes']
        db.delete_index(u'Equipment_part', ['notes_id'])


        # Changing field 'PartCategory.category'
        db.alter_column(u'Equipment_partcategory', 'category', self.gf('django.db.models.fields.CharField')(max_length=75))

    def backwards(self, orm):
        # Adding index on 'Part', fields ['notes']
        db.create_index(u'Equipment_part', ['notes_id'])

        # Adding model 'ClientEstimate'
        db.create_table(u'Equipment_clientestimate', (
            ('margin_guidelines', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('total_flat_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('estimate_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('estimate_client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.Client'])),
            ('job_name', self.gf('django.db.models.fields.TextField')(max_length=45)),
            ('sales_commission', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('prevailing_wage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('is_capital_improvement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('preparer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('margin', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Adding model 'Estimate_Parts_Sales'
        db.create_table(u'Equipment_estimate_parts_sales', (
            ('flat_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('sub_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('part_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.Part'])),
            ('estimate_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.SalesEstimate'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('final_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('total_labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
        ))
        db.send_create_signal(u'Equipment', ['Estimate_Parts_Sales'])

        # Adding model 'Estimate_Parts_Client'
        db.create_table(u'Equipment_estimate_parts_client', (
            ('flat_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('sub_total', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('part_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.Part'])),
            ('estimate_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.ClientEstimate'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('final_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('total_labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
        ))
        db.send_create_signal(u'Equipment', ['Estimate_Parts_Client'])

        # Adding model 'SalesEstimate'
        db.create_table(u'Equipment_salesestimate', (
            ('margin_guidelines', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('total_flat_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('estimate_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('listed_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_profit', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('prevailing_wage', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('estimate_sales', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.SalesProspect'])),
            ('job_name', self.gf('django.db.models.fields.TextField')(max_length=45)),
            ('sales_commission', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('is_capital_improvement', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('preparer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('labor', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('margin', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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

        # Deleting field 'Part.quantity'
        db.delete_column(u'Equipment_part', 'quantity')


        # Renaming column for 'Part.notes' to match new field type.
        db.rename_column(u'Equipment_part', 'notes', 'notes_id')
        # Changing field 'Part.notes'
        db.alter_column(u'Equipment_part', 'notes_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Notes']))

        # Changing field 'PartCategory.category'
        db.alter_column(u'Equipment_partcategory', 'category', self.gf('django.db.models.fields.TextField')())

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
        u'Equipment.camera': {
            'Meta': {'object_name': 'Camera'},
            'camera_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'camera_system_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.System']"}),
            'is_wireless': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'install_guide': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_recalled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'labor': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '300', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'part_manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Vendor.Manufacturer']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '6', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'spec_sheet': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'Equipment.partcategory': {
            'Meta': {'object_name': 'PartCategory'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        }
    }

    complete_apps = ['Equipment']
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table(u'Site_site', (
            ('site_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.Client'])),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('site_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
        ))
        db.send_create_signal(u'Site', ['Site'])

        # Adding M2M table for field site_call_list on 'Site'
        m2m_table_name = db.shorten_name(u'Site_site_site_call_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('site', models.ForeignKey(orm[u'Site.site'], null=False)),
            ('calllist', models.ForeignKey(orm[u'Common.calllist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['site_id', 'calllist_id'])

        # Adding model 'System'
        db.create_table(u'Site_system', (
            ('system_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.Site'])),
            ('system_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('system_client_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.Client'])),
            ('system_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Genre'])),
            ('system_panel_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Equipment.Panel'], null=True, blank=True)),
            ('tampered_id', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('is_system_local', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('panel_location', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('primary_power_location', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('primary_communications', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('secondary_communications', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('backup_communications', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('system_installer_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Installer'], null=True, blank=True)),
            ('master_code', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('lockout_code', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('system_ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('port', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('network_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.Network'])),
        ))
        db.send_create_signal(u'Site', ['System'])

        # Adding model 'Network'
        db.create_table(u'Site_network', (
            ('network_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('router_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('router_user_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('router_password', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('wifi_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('wifi_password', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('wifi_notes', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'Site', ['Network'])

        # Adding model 'Zone'
        db.create_table(u'Site_zone', (
            ('zone_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.System'])),
            ('zone_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('zone_location', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('zone_notes', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_wireless', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Site', ['Zone'])

        # Adding model 'Monitoring'
        db.create_table(u'Site_monitoring', (
            ('monitoring_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mon_system_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.System'])),
            ('mon_company', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('receiver_number', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
        ))
        db.send_create_signal(u'Site', ['Monitoring'])


    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table(u'Site_site')

        # Removing M2M table for field site_call_list on 'Site'
        db.delete_table(db.shorten_name(u'Site_site_site_call_list'))

        # Deleting model 'System'
        db.delete_table(u'Site_system')

        # Deleting model 'Network'
        db.delete_table(u'Site_network')

        # Deleting model 'Zone'
        db.delete_table(u'Site_zone')

        # Deleting model 'Monitoring'
        db.delete_table(u'Site_monitoring')


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
        u'Equipment.panel': {
            'Meta': {'object_name': 'Panel'},
            'installation_manual': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'panel_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel_manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Vendor.Manufacturer']"}),
            'user_manual': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Site.monitoring': {
            'Meta': {'object_name': 'Monitoring'},
            'mon_company': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'mon_system_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.System']"}),
            'monitoring_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver_number': ('django.db.models.fields.IntegerField', [], {'max_length': '11'})
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

    complete_apps = ['Site']
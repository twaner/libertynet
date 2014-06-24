# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'Work_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('building_owner', self.gf('django.db.models.fields.IntegerField')(max_length=11)),
            ('job_client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Client.Client'])),
            ('job_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
        ))
        db.send_create_signal(u'Work', ['Job'])

        # Adding M2M table for field job_employee on 'Job'
        m2m_table_name = db.shorten_name(u'Work_job_job_employee')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm[u'Work.job'], null=False)),
            ('employee', models.ForeignKey(orm[u'Employee.employee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['job_id', 'employee_id'])

        # Adding model 'Task'
        db.create_table(u'Work_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task_ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Work.Ticket'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('created_date', self.gf('django.db.models.fields.DateField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='task created by', to=orm['Employee.Employee'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('is_task_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('task_employee', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task completed by', null=True, to=orm['Employee.Employee'])),
            ('completed_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'Work', ['Task'])

        # Adding model 'Ticket'
        db.create_table(u'Work_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scheduled_date', self.gf('django.db.models.fields.DateField')()),
            ('scheduled_time', self.gf('django.db.models.fields.TimeField')()),
            ('ticket_job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Work.Job'])),
            ('ticket_system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Site.System'])),
            ('description_work', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('ticket_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Contact'])),
            ('signature', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('is_ticket_completed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'Work', ['Ticket'])

        # Adding M2M table for field ticket_employee on 'Ticket'
        m2m_table_name = db.shorten_name(u'Work_ticket_ticket_employee')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ticket', models.ForeignKey(orm[u'Work.ticket'], null=False)),
            ('employee', models.ForeignKey(orm[u'Employee.employee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ticket_id', 'employee_id'])

        # Adding model 'Wage'
        db.create_table(u'Work_wage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wages_employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Employee.Employee'])),
            ('wage_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('lunch_start', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('lunch_end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('hourly_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('gross_wage', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('total_hours', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
        ))
        db.send_create_signal(u'Work', ['Wage'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'Work_job')

        # Removing M2M table for field job_employee on 'Job'
        db.delete_table(db.shorten_name(u'Work_job_job_employee'))

        # Deleting model 'Task'
        db.delete_table(u'Work_task')

        # Deleting model 'Ticket'
        db.delete_table(u'Work_ticket')

        # Removing M2M table for field ticket_employee on 'Ticket'
        db.delete_table(db.shorten_name(u'Work_ticket_ticket_employee'))

        # Deleting model 'Wage'
        db.delete_table(u'Work_wage')


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
        u'Equipment.panel': {
            'Meta': {'object_name': 'Panel'},
            'installation_manual': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'panel_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel_manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Vendor.Manufacturer']"}),
            'user_manual': ('django.db.models.fields.CharField', [], {'max_length': '45'})
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
        },
        u'Work.job': {
            'Meta': {'object_name': 'Job'},
            'building_owner': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Address']"}),
            'job_client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Client.Client']"}),
            'job_employee': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Employee.Employee']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'Work.task': {
            'Meta': {'object_name': 'Task'},
            'completed_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task created by'", 'to': u"orm['Employee.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_task_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'task_employee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task completed by'", 'null': 'True', 'to': u"orm['Employee.Employee']"}),
            'task_ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Work.Ticket']"})
        },
        u'Work.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'description_work': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ticket_completed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'scheduled_date': ('django.db.models.fields.DateField', [], {}),
            'scheduled_time': ('django.db.models.fields.TimeField', [], {}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'ticket_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Common.Contact']"}),
            'ticket_employee': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Employee.Employee']", 'symmetrical': 'False'}),
            'ticket_job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Work.Job']"}),
            'ticket_system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Site.System']"})
        },
        u'Work.wage': {
            'Meta': {'object_name': 'Wage'},
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'gross_wage': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lunch_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'lunch_start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'total_hours': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'wage_date': ('django.db.models.fields.DateField', [], {}),
            'wages_employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Employee.Employee']"})
        }
    }

    complete_apps = ['Work']
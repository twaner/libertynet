# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Title'
        db.create_table(u'Employee_title', (
            ('title_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'Employee', ['Title'])

        # Adding model 'Employee'
        db.create_table(u'Employee_employee', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('middle_initial', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('employee_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emp_number', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('emp_address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Address'])),
            ('emp_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Common.Contact'])),
            ('hire_date', self.gf('django.db.models.fields.DateField')()),
            ('pay_type', self.gf('django.db.models.fields.CharField')(default='HR', max_length=12)),
            ('pay_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2, blank=True)),
            ('is_terminated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('termination_date', self.gf('django.db.models.fields.DateField')(default=None, null=True, blank=True)),
            ('termination_reason', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
        ))
        db.send_create_signal(u'Employee', ['Employee'])

        # Adding M2M table for field emp_title on 'Employee'
        m2m_table_name = db.shorten_name(u'Employee_employee_emp_title')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employee', models.ForeignKey(orm[u'Employee.employee'], null=False)),
            ('title', models.ForeignKey(orm[u'Employee.title'], null=False))
        ))
        db.create_unique(m2m_table_name, ['employee_id', 'title_id'])


    def backwards(self, orm):
        # Deleting model 'Title'
        db.delete_table(u'Employee_title')

        # Deleting model 'Employee'
        db.delete_table(u'Employee_employee')

        # Removing M2M table for field emp_title on 'Employee'
        db.delete_table(db.shorten_name(u'Employee_employee_emp_title'))


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

    complete_apps = ['Employee']
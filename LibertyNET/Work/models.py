from django.db import models
from Common.models import NUMBER_CHOICES

#region Models

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=45)
    building_owner = models.IntegerField(max_length=11)
    job_client = models.ForeignKey('Client.Client')
    job_address = models.ForeignKey('Common.Address')
    # This will generate the M2M table
    job_employee = models.ManyToManyField('Employee.Employee')

    #TODO ==> _unicode_

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    #TODO ==> Can this be M2M ??
    ticket_id = models.ForeignKey('Vendor.Ticket')
    task_name = models.CharField(max_length=45)
    task_created = models.DateField()
    task_creator = models.ForeignKey('Employee.Employee')
    #TODO ==> Order task should be completed in
    task_order = models.IntegerField(choices=NUMBER_CHOICES)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey('Employee.Employee')
    task_completed_date = models.DateField()
    task_notes = models.CharField(max_length=200)

    #TODO ==> _unicode_

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    ticket_job = models.ForeignKey('Vendor.Job')
    ticket_system = models.ForeignKey('Site.System')
    description_work = models.CharField(max_length=500)
    technician_note = models.CharField(max_length=500)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    task_site_contact = models.ForeignKey('Common.Contact')
    ticket_site_signature = models.CharField(max_length=45)
    is_completed = models.BooleanField(default=True)
    ticket_employee = models.ManyToManyField('Employee.Employee')

    #TODO ==> _unicode_

class Wages(models.Model):
    wages_id = models.AutoField(primary_key=True)
    wages_employee_id = models.ForeignKey('Employee.Employee')
    wages_date = models.DateField()
    wages_start_time = models.TimeField()
    wages_lunch_start = models.TimeField()
    wages_lunch_end = models.TimeField()
    wages_end_time = models.TimeField()
    hourly_rate = models.DecimalField(max_length=10, decimal_places=2)
    gross_wage = models.DecimalField(max_length=10, decimal_places=2)
    total_hours = models.DecimalField(max_length=10, decimal_places=2)

    #TODO ==> _unicode_

#endregion
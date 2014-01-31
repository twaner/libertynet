from django.db import models
from Common.models import NUMBER_CHOICES

#region Models


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=45)
    #TODO Should be FK
    building_owner = models.IntegerField(max_length=11)
    job_client = models.ForeignKey('Client.Client')
    job_address = models.ForeignKey('Common.Address')
    # This will generate the M2M table
    job_employee = models.ManyToManyField('Employee.Employee')

    def __str__(self):
        return '%s' % self.job_name


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    #TODO ==> Can this be M2M ??
    task_ticket_id = models.ForeignKey('Work.Ticket')
    task_name = models.CharField(max_length=45)
    task_created_date = models.DateField()
    task_creator = models.ForeignKey('Employee.Employee', related_name="task created by")
    task_order = models.IntegerField(choices=NUMBER_CHOICES)
    is_task_completed = models.BooleanField(default=False)
    task_completed_by = models.ForeignKey('Employee.Employee', related_name="task completed by",
                                          null=True, blank=True)
    task_completed_date = models.DateField(null=True, blank=True)
    #TODO Task Notes as its own model
    task_notes = models.CharField(max_length=200)

    def __str__(self):
        return self.task_name

"""
class Task_Notes(models.Model):
    note_id = models.AutoField(primary_key=True)
    note_date = models.DateField()
    note_title = models.CharField(max_length=50)
    note_creator = models.ForeignKey('Employee.Employee')
    notes = models.CharField(max_length=200)

    def __str__(self):
        return '%' % self.note_title
"""

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    ticket_job = models.ForeignKey('Work.Job')
    ticket_system = models.ForeignKey('Site.System')
    description_work = models.CharField(max_length=500)
    #TODO make this ForeignKey('Work.Task_Notes')
    technician_note = models.CharField(max_length=500)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    task_site_contact = models.ForeignKey('Common.Contact')
    ticket_site_signature = models.CharField(max_length=45, null=True, blank=True)
    is_ticket_completed = models.BooleanField(default=True)
    ticket_employee = models.ManyToManyField('Employee.Employee')

    def __str__(self):
        return '%s' % self.description_work


class Wage(models.Model):
    wages_id = models.AutoField(primary_key=True)
    wages_employee_id = models.ForeignKey('Employee.Employee')
    wages_date = models.DateField()
    wages_start_time = models.TimeField()
    wages_lunch_start = models.TimeField(blank=True, null=True)
    wages_lunch_end = models.TimeField(blank=True, null=True)
    wages_end_time = models.TimeField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    gross_wage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    wages_total_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s' % self.wages_employee_id.first_name

    #endregion
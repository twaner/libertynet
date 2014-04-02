from django.db import models
from datetime import datetime, timedelta, date
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from decimal import Decimal
from Common.models import NUMBER_CHOICES
from Common.helpermethods import time_diff, seconds_to_hours, time_delta_to_str

#region ModelManagers


class JobManager(models.Manager):
    def create_job(self, name, building_owner, job_client, job_address, job_employee):
        job = self.create(name=name, building_owner=building_owner, job_client=job_client,
                          job_address=job_address)
        #job.save(commit=False)
        [job.job_employee.add(e) for e in job_employee]
        job.save()
        assert isinstance(job, Job)
        return job


class TaskManager(models.Manager):
    def create_task(self, task_ticket, name, created_date, creator, order, is_task_completed,
                    task_employee, completed_date, notes):
        task = self.create(task_ticket=task_ticket, name=name, created_date=created_date, creator=creator,
                           order=order, is_task_completed=is_task_completed, task_employee=task_employee,
                           completed_date=completed_date, notes=notes)
        #[task.task_employee.add(t) for t in task_employee_list]
        task.save()
        assert isinstance(task, Task)
        return task


class TicketManager(models.Manager):
    def create_ticket(self, scheduled_date, scheduled_time, ticket_job, ticket_system, description_work,
                      notes, start_date, start_time, end_date, end_time, ticket_contact, signature,
                      is_ticket_completed, ticket_employee):
        ticket = self.create(scheduled_date=scheduled_date, scheduled_time=scheduled_time, ticket_job=ticket_job,
                             ticket_system=ticket_system, description_work=description_work,
                             notes=notes, start_date=start_date, start_time=start_time, end_date=end_date,
                             end_time=end_time, ticket_contact=ticket_contact, signature=signature,
                             is_ticket_completed=is_ticket_completed)
        #ticket.save(commit=False)
        [ticket.ticket_employee.add(t) for t in ticket_employee]
        ticket.save()
        assert isinstance(ticket, Ticket)
        return ticket


class WageManager(models.Manager):
    def create_wage(self, wages_employee, wage_date, start_time, lunch_start, lunch_end, end_time,
                    hourly_rate):
        wage = self.create(wages_employee=wages_employee, wage_date=wage_date, start_time=start_time,
                           lunch_start=lunch_start, lunch_end=lunch_end, end_time=end_time,
                           hourly_rate=hourly_rate)
        took_lunch = False
        worked = False
        # If start and end time to lunch
        if lunch_start == '' or lunch_start is not None and lunch_end == '' or lunch_end is not None:
            lunch = time_diff(lunch_start, lunch_end)
            took_lunch = True
        # If start and end time to work day
        if start_time == '' or start_time is not None and end_time == '' or end_time is not None:
            worked = True
            work_day = time_diff(start_time, end_time)
        # If worked calculate wages
        if worked:
            if took_lunch:
                # take away lunch
                total = work_day - lunch
            else:
                # No lunch
                total = work_day
            wage.total_hours = seconds_to_hours(total)
            wage.gross_wage = round(Decimal(wage.total_hours), 2) * round(Decimal(wage.hourly_rate), 2)

        wage.save()
        assert isinstance(wage, Wage)
        return wage


#endregion

#region Models


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    #TODO Should be FK
    building_owner = models.IntegerField(max_length=11)
    job_client = models.ForeignKey('Client.Client')
    job_address = models.ForeignKey('Common.Address')
    job_employee = models.ManyToManyField('Employee.Employee')

    objects = JobManager()

    def __str__(self):
        return 'Job: %s Client: %s' % (self.name, self.job_client)

    def get_absolute_url(self):
        return reverse('Work:jobdetails', kwargs={'pk': self.id})


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    #TODO ==> Can this be M2M ??
    task_ticket = models.ForeignKey('Work.Ticket')
    name = models.CharField(max_length=45)
    created_date = models.DateField()
    creator = models.ForeignKey('Employee.Employee', related_name="task created by")
    order = models.IntegerField(choices=NUMBER_CHOICES)
    is_task_completed = models.BooleanField(default=False)
    #completed_by
    task_employee = models.ForeignKey('Employee.Employee', related_name="task completed by",
                                      null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    #TODO Task Notes as its own model m2m
    notes = models.CharField(max_length=200)

    objects = TaskManager()

    def __str__(self):
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('Work:taskdetails', kwargs={'pk': self.id})


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    ticket_job = models.ForeignKey('Work.Job')
    ticket_system = models.ForeignKey('Site.System')
    description_work = models.CharField(max_length=500)
    #TODO make this ForeignKey('Work.Task_Notes')
    notes = models.CharField(max_length=500)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    ticket_contact = models.ForeignKey('Common.Contact')
    signature = models.CharField(max_length=45, null=True, blank=True)
    is_ticket_completed = models.BooleanField(default=True)
    ticket_employee = models.ManyToManyField('Employee.Employee')

    objects = TicketManager()

    def __str__(self):
        return '%s' % self.description_work

    def get_absolute_url(self):
        return reverse('Work:ticketdetails', kwargs={'pk': self.id})


class Wage(models.Model):
    id = models.AutoField(primary_key=True)
    wages_employee = models.ForeignKey('Employee.Employee')
    wage_date = models.DateField()
    start_time = models.TimeField()
    lunch_start = models.TimeField(blank=True, null=True)
    lunch_end = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    gross_wage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    objects = WageManager()

    def __str__(self):
        return '%s' % self.wages_employee.first_name

    def get_absolute_url(self):
        return reverse('Work:wagedetails', kwargs={'pk': self.id})

    def clean(self):
        # Cannot have an end time without a start time
        """
        Validation rules for Wage time.
        1: If there is an end time there must be a start time.
        2: If there is an end time for lunch there must be a lunch start time.
        3: Lunch end cannot be earlier than start.
        4: Day end cannot be earlier than day start.
        5: Full day info with no lunch end time.
        @raise ValidationError:
        """
        # print('IN clean()', self.start_time, self.end_time, self.lunch_start, self.lunch_end)
        # print('Clean()', (self.end_time != '' or self.end_time is not None) and (self.start_time == '' or self.start_time is None))
        #if self.end_time != '' or self.end_time is None and self.start_time == '' or self.start_time is None:

        if (self.end_time != '' or self.end_time is not None) and (self.start_time == '' or self.start_time is None):
            raise ValidationError('Cannot have an work ending time without a starting time.')
        #if self.lunch_end != '' or self.lunch_end is None and self.lunch_start == '' or self.lunch_start is None:

        if (self.lunch_end != '' or self.lunch_end is not None) and (
                        self.lunch_start == '' or self.lunch_start is None):
            raise ValidationError('Cannot have an lunch ending time without a starting time.')

        if self.lunch_end <= self.lunch_start:
            raise ValidationError('Lunch start time cannot be later than lunch end.')

        if self.end_time <= self.start_time:
            raise ValidationError('Work start time cannot be later than end time.')

        if self.start_time and self.end_time and self.lunch_start and self.lunch_end == '' or self.lunch_end is None:
            raise ValidationError('Please enter end of lunch time.')

    @property
    def time_worked(self):
        return time_delta_to_str(self.total_hours)

    @property
    def took_lunch(self):
        """
        If both start and end times for Lunch return True else return False.
        @return: Boolean.
        """
        #print('%^%', self.lunch_end == '' or self.lunch_end is None or self.lunch_start == '' or self.lunch_start is None)
        if self.lunch_end == '' or self.lunch_end is None or self.lunch_start == '' or self.lunch_start is None:
            return False
        else:
            return True

    @property
    def lunch_time(self):
        """
        If lunch start and end. Time taken for lunch. Else 0.
        @return: Time taken for lunch.
        """
        # print('lunch_time', self.lunch_end == '', self.lunch_end is None,
        #       self.lunch_start == '', self.lunch_start is None)
        # print('lunch_time2', (self.lunch_end == '' or self.lunch_end is None
        #       and self.lunch_start == '' or self.lunch_start is None))
        if not (self.lunch_end == '' or self.lunch_end is None and self.lunch_start == '' or self.lunch_start is None):
            lunch = time_diff(self.lunch_start, self.lunch_end)
            return lunch
        else:
            return timedelta(hours=0, minutes=0)

            #endregion
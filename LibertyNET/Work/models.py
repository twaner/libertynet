from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from Common.models import NUMBER_CHOICES, Estimate
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
            total_hours = seconds_to_hours(total)
            gross_wage = total_hours * hourly_rate
            wage.total_hours = total_hours
            wage.gross_wage = gross_wage

        wage.save()
        assert isinstance(wage, Wage)
        return wage


class ClientEstimateManager(models.Manager):
    def create_clientestimate(self, job_name, estimate_address, date, preparer, estimate_client,
                              is_capital_improvement, margin, margin_guidelines):

        estimate = self.create(job_name=job_name, estimate_address=estimate_address, date=date,
                               preparer=preparer, is_capital_improvement=is_capital_improvement,
                               total_cost=0.0, total_price=0.0, total_profit=0.0,
                               listed_price=0.0, listed_profit=0.0, estimate_client=estimate_client,
                               labor=0.0, sales_commission=0.0, prevailing_wage=0.0,
                               margin=margin, margin_guidelines=margin_guidelines, total_flat_rate=0.0,
                               custom_sales_commission=0.0)
        estimate.cost = 0.0
        estimate.total_cost = 0.0
        estimate.total_price = 0.0
        estimate.total_profit = 0.0
        estimate.total_flat_rate = 0.0
        estimate.listed_price = 0.0
        estimate.listed_profit = 0.0
        estimate.sales_commission = 0.0
        estimate.labor = 0.0
        estimate.prevailing_wage = 0.0
        estimate.custom_sales_commission = 0.0

        estimate.save()
        return estimate


class EstimatePartsModelManager(models.Manager):
    def create_estimate_parts(self, part_id, quantity, final_cost, cost, sub_total, profit,
                              flat_total, total_labor):
        cost = cost * quantity
        estimate_parts = self.create(part_id=part_id, quantity=quantity, final_cost=final_cost,
                                     cost=cost, sub_total=sub_total, profit=profit,
                                     flat_total=flat_total, total_labor=total_labor)
        estimate_parts.save()
        return estimate_parts


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
        return '%s' % self.name

    def get_absolute_url(self):
        return reverse('Work:jobdetails', kwargs={'pk': self.id})

    def get_absolute_url_edit(self):
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
    task_employee = models.ForeignKey('Employee.Employee', related_name="task completed by",
                                      null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.ForeignKey('Common.Notes')

    objects = TaskManager()

    def __str__(self):
        return '%s' % self.name


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    ticket_job = models.ForeignKey('Work.Job')
    ticket_system = models.ForeignKey('Site.System')
    description_work = models.CharField(max_length=500)
    notes = models.ForeignKey('Common.Notes')
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
        reverse('Work:ticketdetails', kwargs={'pk': self.id})

    def get_absolute_url_edit(self):
        reverse('Work:updateticket', kwargs={'pk': self.id})


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

    def clean(self):
        # Cannot have an end time without a start time
        if self.end_time != '' or self.end_time is None and self.start_time == '' or self.start_time is None:
            raise ValidationError('Cannot have an work ending time without a starting time.')
        if self.lunch_end != '' or self.lunch_end is None and self.lunch_start == '' or self.lunch_start is None:
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

#region Estimate


class ClientEstimate(Estimate):
    estimate_client = models.ForeignKey('Client.Client')
    estimate_parts = models.ManyToManyField('Work.Estimate_Parts_Client')

    objects = ClientEstimateManager()

    def __str__(self):
        return 'Estimate for: %s \n %s' % (self.estimate_client, self.date)

    def get_absolute_url(self):
        return reverse('Work:estimatedetails', kwargs={'pk': self.id})

    def create_estimate(self):
        return reverse('Work:createestimate', kwargs={'pk': self.id})

    def update_estimate(self):
        return reverse('Work:updateestimate', kwargs={'pk': self.id})

    def update_parts(self):
        return reverse('Work:updatepart', kwargs={'pk': self.id})

    def update_part(self):
        return reverse('Work:updatepart', kwargs={'pk': self.id,
                                                  'part_pk': self.estimate_parts.part_id})


class SalesEstimate(Estimate):
    estimate_sales = models.ForeignKey('Client.SalesProspect')
    estimate_parts = models.ManyToManyField('Work.Estimate_Parts_Sales')

    def __str__(self):
        return 'Estimate for: %s \n %s' % (self.estimate_sales, self.date)


class EstimatePartsBase(models.Model):
    part_id = models.ForeignKey('Equipment.Part')
    quantity = models.IntegerField(max_length=6)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total of Cost Plus Margin')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cost of Estimate Part')
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sub Total of Part')
    profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Profit off Part')
    flat_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Flat Price of Part')
    total_labor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Labor for Part')

    class Meta:
        abstract = True

    def update_part(self):
        return reverse('Work:updatepart', kwargs={'pk': self.part_id})


class Estimate_Parts_Client(EstimatePartsBase):
    #estimate_id = models.ForeignKey('Work.ClientEstimate')
    # part_id = models.ForeignKey('Equipment.Part')
    # quantity = models.IntegerField(max_length=6)
    # final_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # cost = models.DecimalField(max_digits=10, decimal_places=2)
    # sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    # profit = models.DecimalField(max_digits=10, decimal_places=2)
    # flat_total = models.DecimalField(max_digits=10, decimal_places=2)
    # total_labor = models.DecimalField(max_digits=10, decimal_places=2)

    objects = EstimatePartsModelManager()


class Estimate_Parts_Sales(EstimatePartsBase):
    estimate_id = models.ForeignKey('Work.SalesEstimate')
    # part_id = models.ForeignKey('Equipment.Part')
    # quantity = models.IntegerField(max_length=6)
    # final_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # cost = models.DecimalField(max_digits=10, decimal_places=2)
    # sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    # profit = models.DecimalField(max_digits=10, decimal_places=2)
    # flat_total = models.DecimalField(max_digits=10, decimal_places=2)
    # total_labor = models.DecimalField(max_digits=10, decimal_places=2)

    objects = EstimatePartsModelManager()

#endregion





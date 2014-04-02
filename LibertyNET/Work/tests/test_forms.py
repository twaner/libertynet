from django.test import TestCase
from Work.factories import JobFactory, TaskFactory, TicketFactory, WageFactory
from Work.models import Job, Task, Ticket, Wage
from Work.forms import JobForm, TaskForm, TicketForm, WageForm
from Work.helpermethods import create_job_helper, create_task_helper, create_ticket_helper, create_wage_helper
from Common.helpermethods import form_assert_false_worker, form_assert_true_worker, form_errors_printer, \
    m2m_to_pk_list, assert_true_worker, assert_equals_worker
from Employee.factories import EmployeeFactory

#region Work Factory


class WorkFormTest(TestCase):
    print('Starting %s....' % TestCase.__name__)

    def test_job_form(self):
        job = JobFactory()
        form = JobForm()
        form_assert_false_worker(self, form)
        # Employee List
        emp = m2m_to_pk_list(job, Job, 'job_employee')
        job_data = {
            'name': job.name, 'building_owner': job.building_owner, 'job_client': job.job_client.client_id,
            'job_address': job.job_address.id, 'job_employee': emp
        }
        form = JobForm(data=job_data)
        form_assert_true_worker(self, form)

    def test_task_form(self):
        task = TaskFactory()
        form = TaskForm()
        form_assert_false_worker(self, form)
        emp = EmployeeFactory()
        emp_id = emp.employee_id
        print('***', emp_id, type(emp_id))
        task_data = {
            'task_ticket': task.task_ticket.id, 'name': task.name, 'created_date': task.created_date,
            'creator': task.creator.employee_id, 'order': task.order, 'is_task_completed': task.is_task_completed,
            'task_employee': emp_id, 'completed_date': task.completed_date, 'notes': task.notes
        }

        form = TaskForm(data=task_data)
        form_assert_true_worker(self, form)

    def test_ticket_form(self):
        ticket = TicketFactory()
        form = TicketForm()
        form_assert_false_worker(self, form)
        emp = m2m_to_pk_list(ticket, Ticket, 'ticket_employee')
        ticket_data = {
            'scheduled_date': ticket.scheduled_date, 'scheduled_time': ticket.scheduled_time,
            'ticket_job': ticket.ticket_job.id, 'ticket_system': ticket.ticket_system.system_id,
            'description_work': ticket.description_work, 'notes': ticket.notes, 'start_date': ticket.start_date,
            'start_time': ticket.start_time, 'end_date': ticket.end_date, 'end_time': ticket.end_time,
            'ticket_contact': ticket.ticket_contact.id, 'signature': ticket.signature,
            'is_ticket_completed': ticket.is_ticket_completed, 'ticket_employee': emp
        }
        form = TicketForm(data=ticket_data)
        form_assert_true_worker(self, form)

    def test_wage_form(self):
        wage = WageFactory()
        form = WageForm()
        form_assert_false_worker(self, form)
        wage_data = {
            'wages_employee': wage.wages_employee.employee_id, 'wage_date': wage.wage_date,
            'start_time': wage.start_time, 'lunch_start': wage.lunch_start, 'lunch_end': wage.lunch_end,
            'end_time': wage.end_time, 'hourly_rate': wage.hourly_rate
        }
        form = WageForm(data=wage_data)
        form_errors_printer(form)
        form_assert_true_worker(self, form)

    def test_wage_form_create_method(self):
        emp = EmployeeFactory()
        wage = WageFactory()

        wage_data = {
            'wages_employee': emp.employee_id, 'wage_date': wage.wage_date,
            'start_time': wage.start_time, 'lunch_start': wage.lunch_start, 'lunch_end': wage.lunch_end,
            'end_time': wage.end_time, 'hourly_rate': wage.hourly_rate
        }
        form = WageForm(data=wage_data)
        if form.is_valid():
            form_assert_true_worker(self, form)
            wage_created = create_wage_helper(form)
            assert_true_worker(self, Wage, wage_created)
        else:
            form_errors_printer(form)

    def test_ticket_form_create_method(self):
        ticket = TicketFactory()
        form = TicketForm()
        form_assert_false_worker(self, form)
        emp = m2m_to_pk_list(ticket, Ticket, 'ticket_employee')
        ticket_data = {
            'scheduled_date': ticket.scheduled_date, 'scheduled_time': ticket.scheduled_time,
            'ticket_job': ticket.ticket_job.id, 'ticket_system': ticket.ticket_system.system_id,
            'description_work': ticket.description_work, 'notes': ticket.notes, 'start_date': ticket.start_date,
            'start_time': ticket.start_time, 'end_date': ticket.end_date, 'end_time': ticket.end_time,
            'ticket_contact': ticket.ticket_contact.id, 'signature': ticket.signature,
            'is_ticket_completed': ticket.is_ticket_completed, 'ticket_employee': emp
        }
        form = TicketForm(data=ticket_data)
        if form.is_valid():
            form_assert_true_worker(self, form)
            ticket_created = create_ticket_helper(form)
            assert_true_worker(self, Ticket, ticket_created)
            assert_equals_worker(self, len(emp), ticket_created.ticket_employee.count())
        else:
            form_errors_printer(form)

    def test_job_form_create_method(self):
        job = JobFactory()
        form = JobForm()
        form_assert_false_worker(self, form)
        # Employee List
        emp = m2m_to_pk_list(job, Job, 'job_employee')
        job_data = {
            'name': job.name, 'building_owner': job.building_owner, 'job_client': job.job_client.client_id,
            'job_employee': emp
        }
        form = JobForm(data=job_data)
        if form.is_valid():
            form_assert_true_worker(self, form)
            job_created = create_job_helper(form, job.job_address)
            assert_true_worker(self, Job, job_created)
            assert_equals_worker(self, len(emp), job_created.job_employee.count())

    def test_task_form_method(self):
        task = TaskFactory()
        form = TaskForm()
        form_assert_false_worker(self, form)
        emp = EmployeeFactory()
        emp_id = emp.employee_id
        print('***', emp_id, type(emp_id))
        task_data = {
            'task_ticket': task.task_ticket.id, 'name': task.name, 'created_date': task.created_date,
            'creator': task.creator.employee_id, 'order': task.order, 'is_task_completed': task.is_task_completed,
            'task_employee': emp_id, 'completed_date': task.completed_date, 'notes': task.notes
        }
        form = TaskForm(data=task_data)
        if form.is_valid():
            form_assert_true_worker(self, form)
            created_task = create_task_helper(form)
            assert_true_worker(self, Task, created_task)

#endregion

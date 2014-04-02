from Work.models import Job, Ticket, Task, Wage
from Common.helpermethods import boolean_helper

#region helpers


def create_job_helper(form, address):
    name = form.cleaned_data.get("name")
    building_owner = form.cleaned_data.get('building_owner')
    job_client = form.cleaned_data.get('job_client')
    job_address = address
    employees = form.cleaned_data.get('job_employee')

    job = Job.objects.create_job(name, building_owner, job_client, job_address, employees)
    return job


def create_task_helper(form):
    task_ticket = form.cleaned_data.get("task_ticket")
    name = form.cleaned_data.get("name")
    created_date = form.cleaned_data.get("created_date")
    creator = form.cleaned_data.get("creator")
    order = form.cleaned_data.get("order")
    is_task_completed = form.cleaned_data.get("is_task_completed")
    task_employee = form.cleaned_data.get("task_employee")
    completed_date = form.cleaned_data.get("completed_date")
    notes = form.cleaned_data.get("notes")

    task = Task.objects.create_task(task_ticket, name, created_date, creator, order, is_task_completed,
                                    task_employee, completed_date, notes)
    return task


def create_ticket_helper(form):
    scheduled_date = form.cleaned_data.get('scheduled_date')
    scheduled_time = form.cleaned_data.get('scheduled_time')
    ticket_job = form.cleaned_data.get('ticket_job')
    ticket_system = form.cleaned_data.get('ticket_system')
    description_work = form.cleaned_data.get('description_work')
    notes = form.cleaned_data.get('notes')
    start_date = form.cleaned_data.get('start_date')
    start_time = form.cleaned_data.get('start_time')
    end_date = form.cleaned_data.get('end_date')
    end_time = form.cleaned_data.get('end_time')
    ticket_contact = form.cleaned_data.get('ticket_contact')
    signature = form.cleaned_data.get('signature')
    is_ticket_completed = boolean_helper(form.cleaned_data.get('is_ticket_completed'))
    # M2M
    ticket_employee = form.cleaned_data.get('ticket_employee')
    #print('TRT', ticket_employee, type(ticket_employee))

    ticket = Ticket.objects.create_ticket(scheduled_date, scheduled_time, ticket_job, ticket_system, description_work,
                                          notes, start_date, start_time, end_date, end_time, ticket_contact, signature,
                                          is_ticket_completed, ticket_employee)
    return ticket


def create_wage_helper(form):
    wages_employee = form.cleaned_data.get('wages_employee')
    wage_date = form.cleaned_data.get('wage_date')
    start_time = form.cleaned_data.get('start_time')
    lunch_start = form.cleaned_data.get('lunch_start')
    lunch_end = form.cleaned_data.get('lunch_end')
    end_time = form.cleaned_data.get('end_time')
    hourly_rate = form.cleaned_data.get('hourly_rate')

    wage = Wage.objects.create_wage(wages_employee, wage_date, start_time, lunch_start, lunch_end,
                                    end_time, hourly_rate)
    return wage
__author__ = 'taiowawaner'
from Work.models import ClientEstimate,Estimate_Parts_Client
from Equipment.models import Part

#region Estimate Helpers


def create_estimate_step_one(form):

    job_name = form.cleaned_data['job_name']
    estimate_address = form.cleaned_data['estimate_address']
    date = form.cleaned_data['date']
    preparer = form.cleaned_data['preparer']
    is_capital_improvement = form.cleaned_data['is_capital_improvement']
    margin = form.cleaned_data['margin']

    estimate = ClientEstimate.objects.create_clientestimate(job_name=job_name, estimate_address=estimate_address,
                                                            date=date, preparer=preparer, is_capital_improvement=is_capital_improvement,
                                                            margin=margin
                                                            )
    return estimate


def add_part_helper(form, estimate):
    part_id = form.cleaned_data['part_id']
    quantity = form.cleaned_data['quantity']
    final_cost = form.cleaned_data['final_cost']
    cost = form.cleaned_data['cost']
    sub_total = form.cleaned_data['sub_total']
    profit = form.cleaned_data['profit']
    flat_total = form.cleaned_data['flat_total']
    total_labor = form.cleaned_data['total_labor']
    estimate_id = form.cleaned_data['estimate_id']

    epc = Estimate_Parts_Client.ob

    estimate.add()


    # return estimate

#endregion



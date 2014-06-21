__author__ = 'taiowawaner'
from Work.models import ClientEstimate

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

#endregion



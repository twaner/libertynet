__author__ = 'taiowawaner'
from django.db.models import Sum
from Work.models import ClientEstimate, SalesEstimate
from Equipment.models import Part


# region EstimateEngine


class EstimateEngine:
    def __init__(self, estimate):
        if type(estimate) is ClientEstimate:
            self.estimate = ClientEstimate.objects.get(pk=estimate.id)
        else:
            self.estimate = SalesEstimate.objects.get(pk=estimate.id)

    def get_aggregate_parts(self):
        """
        Gets all Sum values for dollar amounts of all Estimate Parts.
        @return: Dictionary of values
        """
        cost_dict = self.estimate.estimate_parts.all(). \
            aggregate(Sum('cost'), Sum('final_cost'), Sum('sub_total'), Sum('profit'),
                      Sum('flat_total'), Sum('total_labor'))
        return cost_dict

    def set_estimate_totals(self):
        """
        Sets all dollar values for an Estimate that are related to the Parts
        @param cost_dict: Dictionary of Sums of dollar values in all Estimate_Parts
        @return: Estimate
        """
        cost_dict = self.get_aggregate_parts()
        estimate = self.estimate
        margin = estimate.margin
        estimate.total_cost = cost_dict['cost__sum']
        estimate.cost = cost_dict['cost__sum']
        estimate.total_price = cost_dict['sub_total__sum']
        estimate.total_profit = cost_dict['profit__sum']
        estimate.total_flat_rate = cost_dict['flat_total__sum']
        estimate.labor = cost_dict['total_labor__sum']
        estimate.sales_commission = estimate.total_profit / (1 / margin)
        estimate.listed_profit = estimate.listed_price - estimate.total_cost
        estimate.custom_sales_commission = estimate.listed_price / (1 / margin)
        # Update estimate and return
        estimate.save(update_fields=['total_cost', 'total_price', 'total_profit', 'total_flat_rate',
                                     'listed_price', 'listed_profit', 'sales_commission', 'labor',
                                     'custom_sales_commission'])

        return estimate

    def new_part_checker(self, part):
        """
        Determines if a Part is already attached to an Estimate
        @param estimate: Estimate to be updated.
        @param part: Part to be added or updated.
        @return: False if Part is in Estimate, True if it is not.
        """
        part_list = list(self.estimate.estimate_parts.all())
        for i in part_list:
            #if type(part) == type(i.part_id):
            if part.id == i.part_id.id:
                return False
        else:
                return True

#region JunkCode
#print("estimate_engine - new_part_checker \n Part: '{0}' \n Part.id '{1}' \n Part_list '{2}'".format(part, part.id, part_list))
# print('test junk %s' % i.part_id)
# print('type %s' % type(part) == type(i.part_id))

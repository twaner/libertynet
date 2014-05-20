from models import Site


#region Site helper methods

def create_site_helper(form, client, address, calllist):
    """
    Creates a Client's Site.
    @param form: Site Form.
    @param client: Client object..
    @param address: Address object.
    @param calllist: Call List object.
    @return: Site object.
    """
    site_client = client
    site_call_list = calllist
    site_address = address
    site_name = form.cleaned_data['site_name']

    site = Site.objects.create_client_site(site_client=site_client,
                                           site_address=site_address, site_name=site_name)
    site.site_call_list.add(site_call_list)
    site.save()
    return site


def update_site_helper(form, address, site):
    site_address = address
    site_name = form.cleaned_data['site_name']

    site.save(update_fields=['site_address', 'site_name'])
    return  site
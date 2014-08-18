from models import Site, System


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
    site.site_address = address
    site.site_name = form.cleaned_data['site_name']

    site.save(update_fields=['site_address', 'site_name'])
    return site


#region System


def create_system_helper(form):
    system_site = form.cleaned_data['system_site']
    system_name = form.cleaned_data['system_name']
    system_client = form.cleaned_data['system_client']
    system_type = form.cleaned_data['system_type']
    system_panel = form.cleaned_data['system_panel']
    tampered_id = form.cleaned_data['tampered_id']
    is_system_local = form.cleaned_data['is_system_local']
    panel_location = form.cleaned_data['panel_location']
    primary_power_location = form.cleaned_data['primary_power_location']
    primary_communications = form.cleaned_data['primary_communications']
    secondary_communications = form.cleaned_data['secondary_communications']
    backup_communications = form.cleaned_data['backup_communications']
    system_installer_code = form.cleaned_data['system_installer_code']
    master_code = form.cleaned_data['master_code']
    lockout_code = form.cleaned_data['lockout_code']
    system_ip_address = form.cleaned_data['system_ip_address']
    port = form.cleaned_data['port']
    user_name = form.cleaned_data['user_name']
    password = form.cleaned_data['password']
    network = form.cleaned_data['network']

    system = System.objects.create_system(
        system_site=system_site, system_name=system_name, system_client, system_client,
        system_type=system_type,system_panel=system_panel, tampered_id=tampered_id, is_system_local=is_system_local,
        panel_location=panel_location, primary_power_location=primary_power_location,
        primary_communications=primary_communications, secondary_communications=secondary_communications,
        backup_communications=backup_communications, system_installer_code=system_installer_code, master_code=master_code,
        lockout_code=lockout_code, system_ip_address=system_ip_address, port=port, user_name=user_name,
        network=network)

    return system

#endregion
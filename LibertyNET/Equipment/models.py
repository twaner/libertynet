from django.db import models

#region Base Class
class Equipment(models.Model):
    """
    Base class for any piece of equipment.
    @field name: Name of the equipment.
    @field location: Location of the equipment.
    """
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        abstract = True
#endregion

#region Subclasses
class Device(Equipment):
    """
    Any piece of Equipment. Can be made up of multiple parts.
    """
    device_id = models.AutoField(primary_key=True)
    device_system_id = models.ForeignKey('System.System', blank=True, null=True)
    # Made up of a part. Use in system
    device_location = models.CharField(max_length=45)
    device_part_id = models.ManyToManyField('Equipment.Part')
    device_function = models.CharField(max_length=50)
    device_zone_id = models.ForeignKey('System.Zone', blank=True, null=True)
    camera_id = models.ManyToManyField('Equipment.Camera', blank=True, null=True)

    #TODO - def __unicode__(self):

class Panel(Equipment):
    panel_id = models.AutoField(primary_key=True)
    panel_manufacturer = models.ForeignKey('Vendor.Manufacturer')
    user_manual = models.CharField(max_length=45)
    installation_manual = models.CharField(max_length=45)

    #TODO - def __unicode__(self):

class Part(Equipment):
    part_manufacturer = models.ForeignKey('Vendor.Manufacturer')
    part_number = models.CharField(max_length=45)
    type = models.ForeignKey('Equipment.Type')

    #TODO - def __unicode__(self):

class Camera(Equipment):
    camera_id = models.AutoField(primary_key=True)
    camera_system_id = models.ForeignKey('System.System')
    notes = models.CharField(max_length=100)
    is_wireless = models.BooleanField(default=False)

    #TODO - def __unicode__(self):

#endregion

#region Models


#endregion
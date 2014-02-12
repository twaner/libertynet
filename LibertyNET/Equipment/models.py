from django.db import models

#region ModelManagers


class DeviceManager(models.Manager):
    def create_device(self, name, location, device_system_id, device_location, device_part_id, device_function,
                      device_zone_id, camera_id):
        """
        Creates a Device.
        @type device_zone_id: Device
        @param name: name of device.
        @param location: location (optional).
        @param device_system_id: System Id.
        @param device_location: Location.
        @param device_part_id: Part Id.
        @param device_function: Function of device.
        @param device_zone_id: Zone Id.
        @param camera_id: Camera Id.
        @return: Device.
        """
        device = self.create(device_system_id=device_system_id, device_location=device_location,
                             device_part_id=device_part_id, device_function=device_function,
                             device_zone_id=device_zone_id, camera_id=camera_id,
                             name=name, location=location)
        device.save()
        return device


class PanelManager(models.Manager):
    def create_panel(self, name, location, panel_id, panel_manufacturer, user_manual, installation_manual):
        """
        Creates a Panel.
        @param name: Name.
        @param location: Location.
        @param panel_id: Panel Id.
        @param panel_manufacturer: Manufacturer name.
        @param user_manual: User manual.
        @param installation_manual: Installation manual.
        @return:
        """
        panel = self.create(name=name, location=location, panel_id=panel_id,
                            panel_manufacturer=panel_manufacturer, user_manual=user_manual,
                            installation_manual=installation_manual)
        panel.save()
        return panel


class PartManager(models.Manager):
    def create_manufacturer(self, name, location, part_manufacturer, part_number, genre):
        """
        Creates a Part.
        @rtype : Part
        @param name: Name.
        @param location: Location.
        @param part_manufacturer: Manufacturer.
        @param part_number: Part Number.
        @param type: Party type.
        @return: Part.
        """
        part = self.create(name=name, location=location, part_manufacturer=part_manufacturer,
                           part_number=part_number, genre=genre)
        part.save()
        return part


class CameraManager(models.Manager):
    def create_camera(self, name, location, camera_system_id, notes, is_wireless):
        """
        Creates a Camera.
        @rtype : Camera.
        @param name: name.
        @param location: Location.
        @param camera_system_id: System Id.
        @param notes: Notes.
        @param is_wireless: Is wireless?
        @return:
        """
        camera = self.create(name=name, location=location, camera_system_id=camera_system_id,
                             notes=notes, is_wireless=is_wireless)
        camera.save()
        return camera

#endregion

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
    device_system_id = models.ForeignKey('Site.System', blank=True, null=True)
    # Made up of a part. Use in system
    device_location = models.CharField(max_length=45)
    device_part_id = models.ManyToManyField('Equipment.Part')
    device_function = models.CharField(max_length=50)
    device_zone_id = models.ForeignKey('Site.Zone', blank=True, null=True)
    camera_id = models.ManyToManyField('Equipment.Camera', blank=True, null=True)

    def __str__(self):
        return 'Device: %s' % self.name


class Panel(Equipment):
    panel_id = models.AutoField(primary_key=True)
    panel_manufacturer = models.ForeignKey('Vendor.Manufacturer')
    user_manual = models.CharField(max_length=45)
    installation_manual = models.CharField(max_length=45)

    def __str__(self):
        return 'Panel: %s' % self.name


class Part(Equipment):
    part_manufacturer = models.ForeignKey('Vendor.Manufacturer')
    part_number = models.CharField(max_length=45)
    type = models.ForeignKey('Common.Genre')

    def __str__(self):
        return 'Part: %s' % self.name


class Camera(Equipment):
    camera_id = models.AutoField(primary_key=True)
    camera_system_id = models.ForeignKey('Site.System')
    notes = models.CharField(max_length=100)
    is_wireless = models.BooleanField(default=False)

    def __str__(self):
        return 'Camera: %s' % self.name

#endregion
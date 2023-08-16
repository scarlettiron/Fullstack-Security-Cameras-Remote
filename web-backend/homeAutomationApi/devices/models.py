from django.db import models
from users.models import household

device_types = [('cam', 'Cam'), 
                ('lock', "Lock")]


class device(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=device_types, max_length=50)
    ip_address = models.CharField(max_length=15)
    url = models.CharField(max_length=50, blank=True, null=True)
    pair = models.OneToOneField('devices.device', related_name="+", blank=True, null = True, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    household = models.ForeignKey(household, on_delete=models.CASCADE, blank=True, null=True)
    unit_id = models.CharField(max_length=1000)


class local_server(models.Model):
    household = models.ForeignKey(household, on_delete=models.CASCADE, blank=True, null=True)
    ip = models.CharField(max_length=20)
    name = models.CharField(max_length=100, default='Main')
    unit_id = models.CharField(max_length=1000)
    
    
class device_passcode(models.Model):
    device = models.ForeignKey(device, on_delete=models.CASCADE)
    code = models.IntegerField()
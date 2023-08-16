from django.db import models
from devices.models import device


alert_types = [
    ('intruder', 'Intruder')
]

class alert(models.Model):
    description = models.CharField(max_length=300, blank=True, null=True)
    device = models.ForeignKey(device, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices = alert_types, max_length=50)
    image = models.ImageField(upload_to='alert/images/', blank=True, null=True)    
    

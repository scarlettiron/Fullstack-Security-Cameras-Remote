from django.db import models

from devices.models import device, local_server

error_types = [
    ('socket', 'Socket'),
    ('server', 'Server'),
    ('local server', 'Local server'),
    ('remote server', 'Remote server'),
    ('stream', 'Stream')
]


class error_log(models.Model):
    description = models.CharField(max_length=300)
    device = models.ForeignKey(device, on_delete=models.CASCADE, blank=True, null=True)
    server = models.ForeignKey(local_server,  on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices = error_types, max_length=50)
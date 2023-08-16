from django.contrib import admin
from .models import device, device_passcode, local_server

admin.site.register(device)
admin.site.register(device_passcode)
admin.site.register(local_server)

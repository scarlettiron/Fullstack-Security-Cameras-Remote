from django.contrib import admin
from .models import household, custom_profile, allowed_person

admin.site.register(household)
admin.site.register(custom_profile)
admin.site.register(allowed_person)

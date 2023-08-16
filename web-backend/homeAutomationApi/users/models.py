from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class household(models.Model):
    is_active = models.BooleanField(default=True)


    

class custom_profile(AbstractUser):
    household = models.ForeignKey(household, on_delete=models.CASCADE, blank=True, null=True)
    is_head = models.BooleanField(default=False)
    
    
    
class allowed_person(models.Model):
    name = models.CharField(max_length=200)
    pic = models.ImageField(upload_to = 'static/allowed-persons/')
    household = models.ForeignKey(household, on_delete=models.CASCADE)


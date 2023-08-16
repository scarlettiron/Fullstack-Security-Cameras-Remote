from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users.models import household, custom_profile

@receiver(pre_save, sender = custom_profile)
def create_household(sender, instance, **kwargs):
    if instance.id is None:
        house = household.objects.create()
        instance.household = house
        

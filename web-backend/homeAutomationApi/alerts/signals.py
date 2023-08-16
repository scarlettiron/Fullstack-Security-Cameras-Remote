from .models import alert
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from twilio.rest import Client
from decouple import config


#send sms when there is an alert
@receiver(post_save, sender=alert)
def send_sms(sender, instance, created, **kwargs):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message_body = f"{instance.type} at {instance.device.name}"
        message = client.messages.create(
            body=message_body,
            from_ = settings.TWILIO_NUMBER,
            to = config('TEST_NUMBER')
            )
    except:
        pass
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import wsRouting.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeAutomationApi.settings')


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "https": get_asgi_application(),
  
  "websocket":
        URLRouter(
            wsRouting.routing.websocket_urlpatterns
        )
})

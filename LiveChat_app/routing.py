
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatConsumer


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path,re_path
from .consumers import ChatConsumer
from . import consumers


#application = ProtocolTypeRouter({'websocket': URLRouter([ path('ws/chat/', ChatConsumer.as_asgi()),])})


websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    #re_path("" , ChatConsumer.as_asgi()) , 

    # Add more WebSocket routes if needed
]
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import applications.routing
import jobs.routing
import notifications.routing  
from django.core.asgi import get_asgi_application  
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            applications.routing.websocket_urlpatterns +
            jobs.routing.websocket_urlpatterns +
            notifications.routing.websocket_urlpatterns 
        )
    ),
})

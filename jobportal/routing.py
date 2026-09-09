from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import applications.routing
import jobs.routing
import notifications.routing  
    

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            applications.routing.websocket_urlpatterns +
            jobs.routing.websocket_urlpatterns +
            notifications.routing.websocket_urlpatterns 
        )
    ),
})

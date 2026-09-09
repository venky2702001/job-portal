from django.urls import path
from messaging import views
app_name = "messaging"
urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("sent/", views.sent_messages, name="sent_messages"),
    path("send/", views.send_message, name="send_message"),
    path("<int:message_id>/", views.message_detail, name="message_detail"),
]
from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),
    path("<int:notification_id>/read/", views.mark_as_read, name="mark_as_read"),
    path("<int:notification_id>/read-ajax/", views.mark_as_read_ajax, name="mark_as_read_ajax"),
    path("read-all-ajax/", views.mark_all_as_read_ajax, name="mark_all_as_read_ajax"),
]

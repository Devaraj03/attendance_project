from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("", views.attendance_dashboard, name="dashboard"),
    path("check-in/", views.check_in, name="check_in"),
    path("check-out/", views.check_out, name="check_out"),
    path("break/start/", views.start_break, name="start_break"),
    path("break/end/", views.end_break, name="end_break"),
]

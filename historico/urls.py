from django.urls import path
from .views import dashboard, login

urlpatterns = [
     path("", login.login_view, name="login"),
    path("logout/", login.logout_view, name="logout"),
    path("dashboard/", dashboard.dashboard_view, name="dashboard"),
   
]
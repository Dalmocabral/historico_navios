from django.urls import path
from .views import dashboard, login, cadastrar_navio

urlpatterns = [
    path("", login.login_view, name="login"),
    path("logout/", login.logout_view, name="logout"),
    path("dashboard/", dashboard.dashboard_view, name="dashboard"),
    path("cadastrar_navio/", cadastrar_navio.cadastrar_navio, name="cadastrar_navio"),
   
]
from django.urls import path
from . import views

app_name = 'app_common'

urlpatterns = [
    path('authentication/login', views.Login.as_view(), name = "login")
]
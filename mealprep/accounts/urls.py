from django.urls import path
from django.contrib.auth import views

from . import views as custom_views

app_name = 'accounts'

urlpatterns = [
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('login/', custom_views.user_login, name='user_login'),
]

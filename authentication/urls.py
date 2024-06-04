from .views import RegistrationView
from django.urls import path


urlpattersn = [
    path('register', RegistrationView.as_view(), name="register")
]
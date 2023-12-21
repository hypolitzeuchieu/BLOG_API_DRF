from django.urls import path
from .views import Registerview


urlpatterns = [
    path('register', Registerview.as_view()),
]

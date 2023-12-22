from django.urls import path
from .views import Registerview, LoginUser


urlpatterns = [
    path('register', Registerview.as_view()),
    path('login', LoginUser.as_view()),

]

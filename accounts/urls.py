from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page, name="login_page"),
    path('signup', views.signup_page, name="signup_page"),
    path('created', views.created, name="created"),
    path('verify-telegram', views.verify_telegram),
]
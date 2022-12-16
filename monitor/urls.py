from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="HomePage"),
    path('monitor', views.monitor, name="Monitor"),
    path('monitor/subscribe', views.subscribe, name="Monitor"),
    path('tel', views.sendTel),
    path('viewUsers', views.viewUser),
    path('getPos', views.GetPosList),
]
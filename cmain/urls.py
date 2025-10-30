
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=""),
    path('main', views.main, name="main"),
    path('userlogin', views.userlogin, name="userlogin"),
    path('userlogout', views.userlogout, name="userlogout"),
    path('noperm', views.noperm, name="noperm"),
    path('change-password/', views.custom_change_password, name='change_password'),
]

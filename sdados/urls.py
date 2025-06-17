from django.urls import path
from . import views

urlpatterns = [
    path('lista_sdados', views.lista_sdados, name="lista_sdados"),
]
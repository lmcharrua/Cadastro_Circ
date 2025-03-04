

from django.urls import path
from . import views

urlpatterns = [
    path('lista_cct',views.lista_cct, name="lista_cct"),
    path('ver_circuito/<int:pk>', views.ver_circuito, name='ver_circuito'),
    path('editar_circuito/<int:pk>', views.editar_circuito, name='editar_circuito'),

]

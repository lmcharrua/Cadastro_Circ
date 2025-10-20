

from django.urls import path
from . import views

urlpatterns = [
    path('lista_cartas',views.lista_cartas, name="lista_cartas"),
    #path('ver_carta/<int:pk>', views.ver_carta, name='ver_carta'),
    path('editar_carta/<int:pk>', views.editar_carta, name='editar_carta'),
    path('criar_carta', views.criar_carta, name='criar_carta'),
    #path('downloadc', views.downloadc, name='downloadc'),
]
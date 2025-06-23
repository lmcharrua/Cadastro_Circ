from django.urls import path
from . import views

urlpatterns = [
    path('lista_sdados', views.lista_sdados, name="lista_sdados"),
    path('detalhe_sdados/<int:pk>', views.detalhe_sdados, name="detalhe_sdados"),
    path('edit_sdados/<int:pk>', views.edit_sdados, name="edit_sdados"),
    path('criar_terminacao/<int:pk>', views.criar_terminacao, name="criar_terminacao"),
]
